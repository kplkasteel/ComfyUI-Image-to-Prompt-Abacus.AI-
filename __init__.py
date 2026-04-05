__version__ = "1.0.0"

try:
    from .node import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
    __all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
except (ImportError, ValueError):
    # Handle case where __init__.py is imported outside of a package context
    # (e.g., during pytest collection)
    pass