# uncompyle6 version 3.9.0
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 2.7.18 (v2.7.18:8d21aa21f2, Apr 20 2020, 13:25:05) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: .\betterReticleSize-src\scripts\client\gui\mods\jakLibrary\__init__.py
# Compiled at: 2023-12-31 00:49:43
from .config_parameters import ConfigParameter, ConfigSection, ParameterSettings
from .config_reader import ConfigReader
from .config_validators import isBool
from .lang import getDefaultModLanguage, LANGUAGE_CODE_TO_LANGUAGE_NAME, setLanguage
from .login_notification import LoginNotificationManager
from .util import dotdict
from gui.modsSettingsApi import g_modsSettingsApi
from ..safeloader.decorators import ModLibrary

def isLanguageCode(value):
    return value is not None and value in LANGUAGE_CODE_TO_LANGUAGE_NAME.keys()


_COMMON_CONFIG = ConfigSection('common', [
 ConfigParameter('language', isLanguageCode, getDefaultModLanguage(), ParameterSettings(1, {'type': 'Dropdown', 'text': 'jakLib.language.title', 
    'tooltip': 'jakLib.language.description', 
    'options': map((lambda langName: {'label': langName}), LANGUAGE_CODE_TO_LANGUAGE_NAME.values())}))], 'jakLib.commonSettings', 'jakLib')
_LOGIN_NOTIFICATION_CONFIG = ConfigSection('common', [
 ConfigParameter('loginNotificationEnabled', isBool, False, ParameterSettings(1, {'type': 'CheckBox', 'text': 'jakLib.loginNotificationEnabled.title', 
    'tooltip': 'jakLib.loginNotificationEnabled.description'})),
 ConfigParameter('errorNotificationEnabled', isBool, True, ParameterSettings(1, {'type': 'CheckBox', 'text': 'jakLib.errorNotificationEnabled.title', 
    'tooltip': 'jakLib.errorNotificationEnabled.description'}))], 'jakLib.modname', 'loginNotification', False, True)
_MOD_LINKAGE = 'JakLib'

def _buildCallback(configSectionName, origCallback):

    def apiCallback(newSettings):
        ConfigReader.updateConfig(configSectionName, newSettings)
        origCallback(dotdict(newSettings))

    return apiCallback


@ModLibrary
class JakLib(object):

    def __init__(self):
        self._configs = []
        self._callbacks = {}
        LoginNotificationManager.init()
        self.initializeModWithConfig(_COMMON_CONFIG, self._onLanguageChanged)
        self.initializeModWithConfig(_LOGIN_NOTIFICATION_CONFIG, LoginNotificationManager.onModSettingsChanged)

    def fini(self):
        LoginNotificationManager.fini()

    def initializeModWithConfig(self, configSection, onModSettingsChangedCallback):
        initialConfig = ConfigReader.readConfig(configSection)
        configSection.setInitialValues(initialConfig)
        onModSettingsChangedCallback(initialConfig)
        prefix = configSection.modPrefix
        self._callbacks[prefix] = _buildCallback(configSection.sectionName, onModSettingsChangedCallback)
        self._configs.append(configSection)
        self._refreshModSettings()

    def _refreshModSettings(self):
        template = self._buildModSettings()
        if template is not None:
            g_modsSettingsApi.setModTemplate(_MOD_LINKAGE, template, self._modSettingsChangedCallback)
        return

    def _buildModSettings(self):
        primaryConfig = None
        for config in self._configs:
            if config.isPrimary:
                primaryConfig = config
                break

        if primaryConfig is None:
            return
        else:
            rootTemplate = primaryConfig.toModsSettingsApiTemplate(primaryConfig.modPrefix)
            for config in self._configs:
                if config.isPrimary:
                    continue
                prefix = config.modPrefix
                template = config.toModsSettingsApiTemplate(prefix)
                rootTemplate['column1'].extend(template['column1'])
                rootTemplate['column2'].extend(template['column2'])

            return rootTemplate
            return

    def _modSettingsChangedCallback(self, linkage, newSettings):
        if linkage == _MOD_LINKAGE:
            for prefix in self._callbacks:
                relevantSettings = {}
                for setting in newSettings:
                    if setting == 'enabled' or setting == 'common.enabled':
                        relevantSettings['enabled'] = newSettings[setting]
                    elif setting == 'language' or setting == 'common.language':
                        relevantSettings['language'] = newSettings[setting]
                    elif setting.startswith(prefix):
                        relevantSettings[setting.partition(prefix)[2]] = newSettings[setting]

                self._callbacks[prefix](relevantSettings)

    def _onLanguageChanged(self, newSettings):
        _COMMON_CONFIG.parameters[0].setInitialValue(newSettings.language)
        setLanguage(newSettings.language)
        self._refreshModSettings()
# okay decompiling C:\dev\wot-mods\betterReticleSize-src\scripts\client\gui\mods\jakLibrary\__init__.pyc
