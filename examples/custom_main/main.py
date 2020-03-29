from os.path import exists

from debian_watcher.packages import Packages
from debian_watcher.storage import Storage


# when defining main.py you can define your reporter inside
def custom_reporter(**kwargs):
    # bla bla bla do something with problems
    pass


# you can change the path to the history storage
s = Storage("./shared_host_storage/", max_history=7)
p = Packages(
    storage=s,
    reporter=custom_reporter,
    logfile="debian_watcher.log" # set a logfile to log all the stuff goin on
)

# example source of packages
PACKAGES_FILE = "./packages.txt"
# you can define own way of getting list of packages
if exists(PACKAGES_FILE):
    with open(PACKAGES_FILE) as f:
        lines = f.readlines()
    # only required thing is to pass the list to check_list()
    p.check_list([ln.strip() for ln in lines])
