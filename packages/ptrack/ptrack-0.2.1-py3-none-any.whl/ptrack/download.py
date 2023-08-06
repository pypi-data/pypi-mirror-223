import os
import requests
from rich.text import Text
from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, TimeRemainingColumn, FileSizeColumn, Task, DownloadColumn, TimeElapsedColumn
from ptrack.methods import CustomFileSizeColumn
from datetime import timedelta

import sys
from humanize import naturalsize  # Make sure to install this package using pip





