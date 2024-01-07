from enumerations import Enumeration

SAFELOADER_ATTRIBUTE_NAME = 'JAK_SAFELOADER'
SAFEOVERRIDE_ATTRIBUTE_NAME = 'SAFELOADER_OVERRIDES'
MOD_SAFELOAD_STATUS = Enumeration('Mod safeloading status', [
    'Success',
    'Failure'
])
