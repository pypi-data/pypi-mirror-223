# DO NOT TOUCH THE FOLLOWING LINES:
import pkg_resources

__version__ = tuple(map(int, pkg_resources.require(__name__)[0].version.split(".")))


# IMPORTS WHICH SHOULD APPEAR IN emzed.ext.test2
# AFTER INSTALLING THE PACKAGE:

from .example_module import compute
