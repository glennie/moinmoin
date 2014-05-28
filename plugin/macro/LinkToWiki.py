"""
    MoinMoin - LinkTo Wikipedia Macro

    @copyright: 2011 by Glennie Vignarajah (glennie@glennie.fr)
    @license:   GNU GPL V3.  see http://www.gnu.org for details

    Usage: <<LinkToWiki(notice=notice,label=label,lang=fr)>>
           <<LinkToWiki(notice,label,lang)>>
           <<LinkToWiki(notice)>>

    History:
    - 2011.24.04: First release
"""

from MoinMoin import wikiutil

"""
    Parameters that macro accepts are:
        - notice (the wikipedia notice name)
        - lang  (optionnal wikipedia language, the default is in french)
        - label (optionnal url label. The default is the same as the notice)

    Examples:

    <<LinkToWiki(Moinmoin, Moinmoin on wikipedia french version)>>
    <<LinkToWiki(Moinmoin, Moinmoin on wikipedia english version, en)>>
    <<LinkToWiki(Moinmoin)>>
"""

def macro_LinkToWiki(macro, notice = None, label = None, lang = "fr"):
    f = macro.formatter

    if not notice:
        return f.strong(1) + \
               f.notice('LinkToWiki examples : ') + \
               f.notice('<<LinkToWiki(Moinmoin, Moinmoin on wikipedia french version)>>, ')

    if label is None:
        label = notice
    if lang is None:
        lang = "fr"

    # Escape HTML stuff.
    notice = wikiutil.escape(notice)
    label = wikiutil.escape(label)
    url = '<a class="interwiki" href="http://' + lang + '.wikipedia.org/wiki/' + notice + '" title="' + label + '">' + label + '</a>'
    return url
