# uncompyle6 version 3.9.0
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 2.7.18 (v2.7.18:8d21aa21f2, Apr 20 2020, 13:25:05) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: .\betterReticleSize-src\scripts\client\gui\mods\jakLibrary\config_parameters.py
# Compiled at: 2023-12-31 00:49:50
from debug_utils import LOG_WARNING
from .lang import l10n

class ConfigSection:

    def __init__(self, sectionName, parameters, modNameKey, modPrefix, isPrimary=False, excludeHeader=False):
        self.sectionName = sectionName
        self.parameters = parameters
        self.modNameKey = modNameKey
        self.modPrefix = modPrefix
        self.isPrimary = isPrimary
        self.excludeHeader = excludeHeader
        self._initial_values_set = False

    def get(self):
        return (
         self.sectionName, self.parameters)

    def setInitialValues(self, config):
        for param in self.parameters:
            if param.parameterName in config:
                param.setInitialValue(config[param.parameterName])

        self._initial_values_set = True

    def toModsSettingsApiTemplate(self, prefix):
        self.modDisplayName = l10n(self.modNameKey)
        if self._initial_values_set is False:
            LOG_WARNING('Initial values for ' + self.modDisplayName + ' have not been set! Using default values instead')
        template = {'modDisplayName': self.modDisplayName, 'column1': [], 'column2': []}
        for configParameter in self.parameters:
            parameterTemplate = configParameter.settingsTemplate.getTemplate()
            parameterTemplate['varName'] = prefix + configParameter.parameterName
            if 'value' not in parameterTemplate:
                parameterTemplate['value'] = configParameter.defaultValue
            if configParameter.settingsTemplate.column == 2:
                template['column2'].append(parameterTemplate)
            else:
                template['column1'].append(parameterTemplate)

        return template


def ModsSettingsApiHeader(modNameKey, col=1, width=1):
    if modNameKey is None:
        return
    else:
        template = {'column1': [], 'column2': []}
        settingsTemplate = {'type': 'Label', 'text': l10n(modNameKey), 
           'tooltip': 'hi'}
        if col == 1:
            template['column1'].append(settingsTemplate)
        else:
            template['column2'].append(settingsTemplate)
        if width == 2:
            if col == 1:
                template['column2'].append({'type': 'Empty'})
            else:
                template['column1'].append({'type': 'Empty'})
        return template
        return


class ConfigParameter:

    def __init__(self, parameterName, validationFunction, defaultValue, settingsTemplate):
        self.parameterName = parameterName
        self.validationFunction = validationFunction
        self.defaultValue = defaultValue
        self.settingsTemplate = settingsTemplate

    def get(self):
        return (
         self.parameterName, self.validationFunction, self.defaultValue)

    def setInitialValue(self, value):
        self.settingsTemplate._template['value'] = value


class ParameterSettings:

    def __init__(self, column, template):
        self.column = column
        self._template = template

    def getTemplate(self):
        template = self._template.copy()
        for localizedKey in ['text', 'tooltip']:
            if template.get(localizedKey, None) is not None:
                template[localizedKey] = l10n(template[localizedKey])

        return template
# okay decompiling C:\dev\wot-mods\betterReticleSize-src\scripts\client\gui\mods\jakLibrary\config_parameters.pyc
