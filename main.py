from os.path import exists

from debian_watcher.packages import Packages
from debian_watcher.storage import Storage

PACKAGES_FILE = "./packages.txt"

try:
    from reporter import custom_reporter
    print("Found a custom reporter")
except ImportError:
    custom_reporter = None

s = Storage("./storage/", max_history=7)
p = Packages(storage=s, reporter=custom_reporter)

if exists(PACKAGES_FILE):
    with open(PACKAGES_FILE) as f:
        lines = f.readlines()
    p.check_list([ln.strip() for ln in lines])
else:
    p.check_all()
