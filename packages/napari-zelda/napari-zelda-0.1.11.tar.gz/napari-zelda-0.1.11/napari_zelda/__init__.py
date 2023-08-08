
try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

from napari_plugin_engine import napari_hook_implementation

@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    from .napari_zelda import launch_ZELDA
    
    return launch_ZELDA
