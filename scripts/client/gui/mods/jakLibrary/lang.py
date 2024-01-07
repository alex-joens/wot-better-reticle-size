# uncompyle6 version 3.5.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.2 (default, Dec 29 2018, 06:19:36) 
# [GCC 7.3.0]
# Embedded file name: .\betterReticleSize-src\scripts\client\gui\mods\jakLibrary\lang.py
# Compiled at: 2023-12-31 16:54:01
from .util import parseLangFields
from collections import OrderedDict
from constants import DEFAULT_LANGUAGE
from debug_utils import LOG_ERROR
from helpers import getClientLanguage
LANGUAGE_CODES = ('be', 'bg', 'cs', 'da', 'de', 'el', 'en', 'es', 'es_ar', 'et', 'fi',
                  'fr', 'hr', 'hu', 'id', 'it', 'ja', 'kk', 'ko', 'lt', 'lv', 'nl',
                  'no', 'pl', 'pt', 'pt_br', 'ro', 'ru', 'sr', 'sv', 'th', 'tr',
                  'uk', 'vi', 'zh_cn', 'zh_sg', 'zh_tw')
LANGUAGE_CODE_TO_LANGUAGE_NAME = OrderedDict([
 ('bg', 'Български'),
 ('be', 'Беларуск'),
 ('cs', 'Čeština'),
 ('da', 'Dansk'),
 ('de', 'Deutsch'),
 ('el', 'Ελληνικά'),
 ('en', 'English'),
 ('es', 'Español'),
 ('es_ar', 'Español (América Latina)'),
 ('et', 'Eesti'),
 ('fi', 'Suomi'),
 ('fr', 'Français'),
 ('hr', 'Hrvatski'),
 ('hu', 'Magyar'),
 ('id', 'Indonesia'),
 ('it', 'Italiano'),
 ('ja', '日本語'),
 ('kk', 'Қазақ тілі'),
 ('ko', '한국인'),
 ('lt', 'Lietuvių'),
 ('lv', 'Latviešu'),
 ('nl', 'Nederlands'),
 ('no', 'Norsk'),
 ('pl', 'Polski'),
 ('pt', 'Português (EU)'),
 ('pt_br', 'Português (BR)'),
 ('ro', 'Română'),
 ('ru', 'Русский'),
 ('sr', 'Srpski'),
 ('sv', 'Svenska'),
 ('th', 'ไทย'),
 ('tr', 'Türkçe'),
 ('uk', 'Українська'),
 ('vi', 'Tiếng Việt'),
 ('zh_cn', '简体中文'),
 ('zh_sg', '简体中文（新加坡）'),
 ('zh_tw', '繁体中文')])
LANGUAGE_FILE_PATH = 'mods/Jak_Atackka.jakLib/text/%s.yml'
DEFAULT_UI_LANGUAGE = 'en'
_LANGUAGE = {}
_LANGUAGES = {}
__all__ = ('getDefaultModLanguage', 'l10n', 'l10nOrNone', 'setLanguage')
for langCode in LANGUAGE_CODES:
    _LANGUAGES[langCode] = parseLangFields(LANGUAGE_FILE_PATH % langCode)

def setLanguage(newLangCodeOrIndex):
    global _LANGUAGE
    newLangCode = getLanguageCodeFromIndex(newLangCodeOrIndex) if type(newLangCodeOrIndex) is int else newLangCodeOrIndex
    if newLangCode in _LANGUAGES.keys():
        _LANGUAGE = _LANGUAGES[newLangCode]
    elif DEFAULT_LANGUAGE in _LANGUAGES.keys():
        _LANGUAGE = _LANGUAGES[DEFAULT_LANGUAGE]
    else:
        _LANGUAGE = _LANGUAGES[DEFAULT_UI_LANGUAGE]


def getDefaultModLanguage():
    clientLanguage = getClientLanguage()
    if clientLanguage in _LANGUAGES.keys():
        return clientLanguage
    else:
        if DEFAULT_LANGUAGE in _LANGUAGES.keys():
            return DEFAULT_LANGUAGE
        return DEFAULT_UI_LANGUAGE


def getLanguageIndexFromCode(langCode):
    if type(langCode) is int:
        return langCode
    try:
        return list(LANGUAGE_CODE_TO_LANGUAGE_NAME.keys()).index(langCode)
    except:
        LOG_ERROR('[SAFELOADER] Unable to find index of lang code: ' + str(langCode))
        return list(LANGUAGE_CODE_TO_LANGUAGE_NAME.keys()).index(getDefaultModLanguage())


def getLanguageCodeFromIndex(index):
    if type(index) is not int:
        if index.isdigit():
            index = int(index)
        else:
            return index
    try:
        return LANGUAGE_CODE_TO_LANGUAGE_NAME.keys()[index]
    except:
        LOG_ERROR('[SAFELOADER] Unable to find lang code for index: ' + str(langCode))
        return getDefaultModLanguage()


def l10n(key):
    """returns localized value relative to key"""
    result = key
    if key in _LANGUAGE:
        result = _LANGUAGE[key]
    elif key in _LANGUAGES[DEFAULT_UI_LANGUAGE]:
        result = _LANGUAGES[DEFAULT_UI_LANGUAGE][key]
    return result


def l10nOrNone(key):
    result = None
    if key in _LANGUAGE:
        result = _LANGUAGE[key]
    elif key in _LANGUAGES[DEFAULT_UI_LANGUAGE]:
        result = _LANGUAGES[DEFAULT_UI_LANGUAGE][key]
    return result


setLanguage(getClientLanguage())