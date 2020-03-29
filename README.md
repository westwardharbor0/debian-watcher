<strong>this is a first version, big changes will be done in next commits
</strong>

# DEBIAN WATCHER
Purpose of this script is to track changes of your debian packages
<br>
If any changes happen you can define your own reporter method which can contain for example `sentry` trigger

# Usage
## venv
If you want to run `debian_watcher` using python3 venv run: 
- `make bootstrap`
- `make run`

## docker
If you want to run `debian_watcher` using docker run:
- `make docker-build`
- `make docker-run` or `make debug-docker-run` (for development purposes)

# Customization
Default behavior: 
- if `packages.txt` not found, checks all deb packages
- stores 20 last changes of a package
- reporting is done in console

Changes to run can be done trough editing `main.py`

To specify packages to check create `pacakges.txt` in root dir with package name on each line

To specify custom reporter create file `reporter.py` in root dir with definition of method `custom_reporter(**kwargs)`
`custom_reporter` method will be called every time there is a change 
