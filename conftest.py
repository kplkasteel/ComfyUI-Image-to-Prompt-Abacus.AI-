# Root conftest.py to prevent pytest from trying to import __init__.py
# This prevents the "attempted relative import with no known parent package" error
# when pytest discovers the parent directory's __init__.py
