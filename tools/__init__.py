import os

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
SRC_DIR = os.path.join(PROJECT_DIR, "src")
TEST_DIR = os.path.join(PROJECT_DIR, "test")

from . import helpers
