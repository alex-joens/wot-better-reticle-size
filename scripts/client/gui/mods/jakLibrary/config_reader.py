# uncompyle6 version 3.9.0
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 2.7.18 (v2.7.18:8d21aa21f2, Apr 20 2020, 13:25:05) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: .\betterReticleSize-src\scripts\client\gui\mods\jakLibrary\config_reader.py
# Compiled at: 2023-12-31 00:49:56
import json, os, threading
from debug_utils import LOG_ERROR, LOG_WARNING
from .lang import getLanguageCodeFromIndex, getLanguageIndexFromCode
from .util import dotdict
from ..safeloader.decorators import ModLibrary
CONFIG_FILE_DIR = './mods/configs/jak_atackka'
CONFIG_FILE_NAME = 'config.json'
CONFIG_FILE_PATH = os.path.join(CONFIG_FILE_DIR, CONFIG_FILE_NAME)

@ModLibrary
class ConfigReader(object):
    __lock = threading.Lock()

    def __init__(self):
        with self.__lock:
            self.__config = {}
            try:
                if not os.path.isdir(CONFIG_FILE_DIR):
                    os.makedirs(CONFIG_FILE_DIR)
                if not os.path.isfile(CONFIG_FILE_PATH):
                    self.__writeEmptyConfig()
            except Exception:
                LOG_ERROR('Failed to create new config')
                return

            configFile = None
            try:
                configFile = open(CONFIG_FILE_PATH, 'r+')
            except Exception:
                LOG_ERROR('Failed to open config file')
                return

            try:
                try:
                    self.__config = json.load(configFile)
                except Exception:
                    LOG_WARNING('Failed to parse config file')
                    self.__writeEmptyConfig()

            finally:
                configFile.close()

        return

    def readConfig(self, sections):
        if not isinstance(sections, list):
            sections = [sections]
        with self.__lock:
            anyChanges = False
            for configSection in sections:
                sectionKey, configParameters = configSection.get()
                if self.__config.get(sectionKey) is None:
                    self.__config[sectionKey] = {}
                for parameter in configParameters:
                    key, validator, defaultValue = parameter.get()
                    if key not in self.__config[sectionKey] or validator(self.__config[sectionKey].get(key)) is False:
                        self.__config[sectionKey][key] = defaultValue
                        anyChanges = True

            if anyChanges:
                self.__updateConfig()
        parsedSections = []
        for configSection in sections:
            parsedSection = dotdict(self.__config[configSection.sectionName])
            if parsedSection.get('language', None) is not None:
                parsedSection.language = getLanguageIndexFromCode(parsedSection.language)
            parsedSections.append(parsedSection)

        if len(parsedSections) == 1:
            return parsedSections[0]
        else:
            return parsedSections
            return

    def updateConfig(self, sectionName, newParams):
        with self.__lock:
            anyChanges = False
            for paramName in newParams:
                if sectionName != 'common' and paramName == 'enabled':
                    continue
                if paramName not in self.__config[sectionName] or self.__config[sectionName][paramName] != newParams[paramName]:
                    newValue = newParams[paramName]
                    if paramName == 'language':
                        newValue = getLanguageCodeFromIndex(newValue)
                    self.__config[sectionName][paramName] = newValue
                    anyChanges = True

            if anyChanges:
                self.__updateConfig()

    def __writeEmptyConfig(self):
        try:
            try:
                f = open(CONFIG_FILE_PATH, 'w')
                f.write('{}')
            except Exception as ex:
                LOG_ERROR('Failed to write empty config')
                raise ex

        finally:
            f.close()

    def __updateConfig(self):
        try:
            try:
                configFile = open(CONFIG_FILE_PATH, 'r+')
                configFile.truncate(0)
                configFile.seek(0)
                configFile.write(json.dumps(self.__config, indent=4))
            except Exception as ex:
                LOG_ERROR('Failed to update config file')
                raise ex

        finally:
            configFile.close()
# okay decompiling C:\dev\wot-mods\betterReticleSize-src\scripts\client\gui\mods\jakLibrary\config_reader.pyc
