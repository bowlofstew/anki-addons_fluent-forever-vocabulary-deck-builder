# -*- coding: utf-8 -*-
# Copyright: Simone Gaiarin <simgunz@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/licenses/gpl.html

from configobj import ConfigObj

from aqt.qt import *
#FIXME: Is uic present in default installation?
from PyQt4 import uic

class Preferences(QDialog):

    def __init__(self, mw):
        QDialog.__init__(self, mw)
        self.mw = mw
        #Dynamically loads the ui
        uic.loadUi(mw.pm.addonFolder() + '/ffvocdeckbuilder/ui/preferences.ui', self);
        #These two instructions run the dialog as modal dialog
        self.loadLanguageCodes()
        languages = sorted(self.languageCodesForward.values())
        self.cbPreferredLanguage.addItems(languages)
        self.cbSecondaryLanguage.addItems(languages)
        self.setModal(True)

        #Load user config
        self.user = self.mw.pm.name
        self.config = ConfigObj('ffvdb.ini')
        if self.config.has_key(self.user ):
            self.leApiForvo.setText(self.config[self.user ]['APIs']['forvo'])
            self.leApiBing.setText(self.config[self.user ]['APIs']['bing'])
            self.cbPreferredLanguage.lineEdit().setText(self.languageCodesForward[self.config[self.user ]['Languages']['Primary']])
            self.cbSecondaryLanguage.lineEdit().setText(self.languageCodesForward[self.config[self.user ]['Languages']['Secondary']])

        self.exec_()

    def accept(self):
        if not self.config:
            self.config = ConfigObj('ffvdb.ini')
        if not self.config.has_key(self.user ):
            self.config[self.user ] = {'APIs': {}, 'Languages': {}}
        self.config[self.user ]['APIs']['forvo'] = self.leApiForvo.text()
        self.config[self.user ]['APIs']['bing'] = self.leApiBing.text()
        self.config[self.user ]['Languages']['Primary'] = self.languageCodesBackward[self.cbPreferredLanguage.currentText()]
        self.config[self.user ]['Languages']['Secondary'] = self.languageCodesBackward[self.cbSecondaryLanguage.currentText()]
        self.config.write()
        self.done(0)

    def reject(self):
        self.done(1)

    def loadLanguageCodes(self):
        self.languageCodesForward = {}
        self.languageCodesBackward = {}
        fileName = u"{0}/ffvocdeckbuilder/files/iso-639-1-language-codes" \
            .format(self.mw.pm.addonFolder())
        with open(fileName) as f:
            for line in f:
                (code, language) = line.split(',')
                code = code.rstrip('\n')
                self.languageCodesForward[code] = language
                self.languageCodesBackward[language] = code
