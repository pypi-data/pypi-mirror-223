# isort: skip_file

# This is the module that test_patching.py uses to test patch_submodule()

import os  # noqa: F401 - this is just for tests
import os as renamed_os  # noqa: F401 - this is just for tests
from os import path  # noqa: F401 - this is just for tests
from os import path as renamed_path  # noqa: F401 - this is just for tests
from os.path import join  # noqa: F401 - this is just for tests
from os.path import join as renamed_join  # noqa: F401 - this is just for tests


open = open  # noqa we just need to have a builtin inside this module to test it properly
