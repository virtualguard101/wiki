import os
import subprocess
import logging
import colorlog
import json
import hashlib
from pathlib import Path
from datetime import datetime
from git import Repo
from mkdocs.config.defaults import MkDocsConfig
