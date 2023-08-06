import os

PLUGIN_DIR = os.path.dirname(__file__)

JOBS_COLOR = "#553198"
JOBS_COLOR_DARK = "#392165"
JOBS_GRADIENT = f"qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {JOBS_COLOR_DARK},  stop: 0.3 {JOBS_COLOR},  stop: 0.7 {JOBS_COLOR}, stop:1 {JOBS_COLOR_DARK})"

MD5_COLOR = "#3e36cf"
MD5_COLOR_DARK = "#2e2e7f"
MD5_GRADIENT = f"qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {MD5_COLOR_DARK},  stop: 0.3 {MD5_COLOR},  stop: 0.7 {MD5_COLOR}, stop:1 {MD5_COLOR_DARK})"

UPLOAD_COLOR = "#2b7418"
UPLOAD_COLOR_DARK = "#1c4910"
UPLOAD_GRADIENT = f"qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {UPLOAD_COLOR_DARK},  stop: 0.3 {UPLOAD_COLOR},  stop: 0.7 {UPLOAD_COLOR}, stop:1 {UPLOAD_COLOR_DARK})"

MD5_CACHE_COLOR = "#553198"
MD5_CACHE_COLOR_DARK = "#392165"
MD5_CACHE_GRADIENT = f"qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {MD5_CACHE_COLOR_DARK},  stop: 0.3 {MD5_CACHE_COLOR},  stop: 0.7 {MD5_CACHE_COLOR}, stop:1 {MD5_CACHE_COLOR_DARK})"

UPLOAD_CACHE_COLOR = "#7C45C4"
UPLOAD_CACHE_COLOR_DARK = "#553198"
UPLOAD_CACHE_GRADIENT = f"qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {UPLOAD_CACHE_COLOR_DARK},  stop: 0.3 {UPLOAD_CACHE_COLOR},  stop: 0.7 {UPLOAD_CACHE_COLOR}, stop:1 {MD5_CACHE_COLOR_DARK})"

OFF_COLOR = "#555"
OFF_COLOR_DARK = "#373737"
OFF_GRADIENT = f"qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {OFF_COLOR_DARK},  stop: 0.3 {OFF_COLOR},  stop: 0.7 {OFF_COLOR}, stop:1 {OFF_COLOR_DARK})"
