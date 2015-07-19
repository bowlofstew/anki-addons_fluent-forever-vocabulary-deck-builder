# -*- coding: utf-8 -*-
#########################################################################
# Copyright (C) 2015 by Simone Gaiarin <simgunz@gmail.com>              #
#                                                                       #
# This program is free software; you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation; either version 3 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program; if not, see <http://www.gnu.org/licenses/>.  #
#########################################################################

import json
import os
import re
import urllib
from urllib import urlretrieve
from bs4 import BeautifulSoup

from extmodules.tempdir import tempdir

#FIXME: These command added because KDevelop default encoding is Ascii??
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

_currentLanguage='XX'

class IpaManager:
    def __init__(self, editor):
        self.editor = editor
        self.webMainFrame = self.editor.web.page().mainFrame()
        self.ipa = {}
        self.loadLanguageCodes()

    def loadLanguageCodes(self):
        self.languageCodes = {}
        fileName = u"{0}/ffvocdeckbuilder/files/iso-639-1-language-codes" \
            .format(self.editor.mw.pm.addonFolder())
        with open(fileName) as f:
            for line in f:
                (key, val) = line.split(',')
                self.languageCodes[key] = val.rstrip('\n')

    def downloadIpa(self, word):
        found = list()
        if not self.ipa.has_key(word):
            url = u'https://en.wiktionary.org/wiki/{0}'.format(word)
            r = urllib.urlopen(url).read()
            soup = BeautifulSoup(r)
            rawIpa = soup.find_all("span", class_="IPA")
            for s in rawIpa:
                foundIpaLanguage = s.findPrevious('h2').span.get_text()
                if re.match(self.languageCodes[_currentLanguage], foundIpaLanguage):
                    found.append({'provider': 'Wen', 'ipa' : s.get_text()})
                    a = s.findPrevious('span', id=re.compile('Etymology_\d+'))
                    if a:
                        found[-1]['spec'] = a.get_text()
            self.ipa[word] = found

    def buildGallery(self, word, nThumbs=5):
        if not self.ipa.has_key(word):
            self.downloadIpa(word)
        gallery = u'<div id="ipagallery">'
        gallery += u'<select id="ipaselector" name="example">'
        for i, v in enumerate(self.ipa[word]):
            gallery += u'<option value="{2}">{0} ({1}'.format(v['ipa'], v['provider'], i)
            print gallery
            if v.has_key('spec'):
                gallery += u', {0}'.format(v['spec'])
            gallery += u')</option>'
        gallery += u'</select></div>'
        self.webMainFrame.findFirstElement("#f6").setOuterXml(gallery)
