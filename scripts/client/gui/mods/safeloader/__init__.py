from gui import mods
from gui.game_loading import loading as gameLoading
from .constants import SAFELOADER_ATTRIBUTE_NAME
from .loader import Safeloader
SAFELOADER = Safeloader()

def _injectSafeloaderIfNotInjectedYet():
    if not hasattr(mods, SAFELOADER_ATTRIBUTE_NAME):
        setattr(mods, SAFELOADER_ATTRIBUTE_NAME, SAFELOADER)
        regular_step = getattr(gameLoading, 'step')

        def new_step():
            setattr(gameLoading, 'step', regular_step)
            safeloader = getattr(mods, SAFELOADER_ATTRIBUTE_NAME)
            safeloader.loadMods()
            print '[SAFELOADER] All mods have been loaded!'
            regular_step()

        setattr(gameLoading, 'step', new_step)


_injectSafeloaderIfNotInjectedYet()
