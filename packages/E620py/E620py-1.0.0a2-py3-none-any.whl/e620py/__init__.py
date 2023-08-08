__version__ = '1.0.0-a2'
__user_agent__ = f"E620py/{__version__} (by mrcrabs)"

import logging
from . import networking
from . import handlers
from . import utils
from . import exceptions

logging.getLogger(__name__).addHandler(logging.NullHandler())
