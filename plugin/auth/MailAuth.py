# -*- coding: iso-8859-1 -*-
#vim: filetype=python syntax=python ai tabstop=4 expandtab shiftwidth=4 smarttab softtabstop=4:
"""
  MoinMoin - Remote mail authentification module.
  This module supports the following schems:
    - pop
    - imap
    

  This code only creates a user object, the session will be established by
  moin automatically.

  @copyright: 2010 Glennie Vignarajah (glennie@glennie.fr)
  @license: GNU GPL V3 or later.
"""

from MoinMoin import log
from MoinMoin import user
from MoinMoin.auth import BaseAuth, CancelLogin, ContinueLogin
import sys,os
logging = log.getLogger(__name__)

class MailAuth(BaseAuth):
  """ Get authentication data from form, authenticate against an imap or pop server, creates a user object for that user. The session is kept by moin automatically.
  """
  login_inputs = ['username', 'password']
  logout_possible = True
  name = 'MailAuth'

#{{{ init
  def __init__(self, url='imap://localhost', autocreate=True, force_https=True, hint='You must use your existing account to log in.'):
    self.autocreate = autocreate
    self.url = url
    self.force_https = force_https
    self.hint = hint
    s_url=url.split(':',3)

    if s_url[0] == '':
      self.scheme = s_url[0]
    else:
      self.scheme = 'imap'

    if len(s_url) > 1:
      self.server=s_url[1].replace('/','')
    else:
      self.server='localhost'

    if len(s_url) > 2:
      self.port = s_url[2].replace('/','')
    else:
      self.port = ''
#}}}

#{{{Login
  def login(self, request, user_obj, **kw):

    connected = False
    u = None
    _ = request.getText
    username = kw.get('username')
    password = kw.get('password')

#{{{ use https for login?
    if (self.force_https) and (request.url.split(':',1)[0] != 'https'):
      return CancelLogin(_('You must use a secure link (https) in order to login'))
#}}}

#{{{ Quit this authentification module if username or password is empty
    if not username: 
      return ContinueLogin(user_obj,_('Missing login.'))

    if not password:
      return ContinueLogin(user_obj,_('Missing password.'))
#}}}

#{{{if the server value is set?
    if self.server == '':
      logging.error('IMAP library not found')
      return ContinueLogin(user_obj,_('An exception occured!'))
#}}}
    

#{{{ Try to authentificate 
    if self.scheme == 'imap':
#{{{
      if self.port.isdigit():
        port = int(self.port)
      else:
        port = 143
      try:
        import imaplib
        imap = imaplib.IMAP4(self.server,port)
        try:
          imap.login(username,password)
          connected = True
          imap.close
        except imap.error, err:
          logging.error('Login failed!')
          return ContinueLogin(user_obj,_('Login failed!'))
      except ImportError, err:
        logging.error('IMAP library not found')
        return ContinueLogin(user_obj,_('An exception occured'))
#}}}

    elif self.scheme == 'pop':
#{{{
      if self.port.isdigit():
        port = int(self.port)
      else:
        port = 110
      try:
        import poplib
        pop = poplib.POP3(self.server,port)
        try:
          pop.user(username)
          pop.pass_(password)
          connected = True
          pop.quit
        except:
          logging.error('Login failed!')
          return ContinueLogin(user_obj,_('Login failed!'))
      except ImportError, err:
        logging.error('POP3 library not found')
        return ContinueLogin(user_obj,_('An exception occured'))
#}}}

    else:
#{{{ unknown scheme
      logging.error('Unknown authentificaion scheme')
      return ContinueLogin(user_obj,_('Login failed: unknown authentificaion scheme'))
      
#}}}
#}}}

#{{{check if we were connected to remote server and create the user object
    if connected:
      u = user.User(request, auth_username=username, auth_method=self.name)
      u.username = username
      u.remember_me = 1
      if self.autocreate and u:
        u.create_or_update(True)
      return ContinueLogin(u)
    else:
      logging.error("Login failed: incorrect login or password!")
      return ContinueLogin(user_obj,_('Login failed: incorrect login or password'))
#}}}

#}}}

#{{{Login hint
  def login_hint(self, request):
    return self.hint
#}}}
