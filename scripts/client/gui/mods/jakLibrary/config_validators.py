# uncompyle6 version 3.9.0
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 2.7.18 (v2.7.18:8d21aa21f2, Apr 20 2020, 13:25:05) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: .\betterReticleSize-src\scripts\client\gui\mods\jakLibrary\config_validators.py
# Compiled at: 2023-12-31 00:50:04


def isBool(value):
    return value is not None and isinstance(value, bool)


def isNumberBetween(min, max):

    def isNumberBetween(value):
        if value is None or not isinstance(value, (int, float)):
            return False
        if value < min or value > max:
            return False
        return True

    return isNumberBetween


def isNumberBetweenZeroAndOne(value):
    return isNumberBetween(0, 1)(value)
# okay decompiling C:\dev\wot-mods\betterReticleSize-src\scripts\client\gui\mods\jakLibrary\config_validators.pyc
