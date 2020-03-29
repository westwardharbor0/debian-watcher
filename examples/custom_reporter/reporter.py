from sentrysdk import init, capture_message

# prepare sentry env
init(dsn='https://<key>@sentry.io/<project>')


# define a method custom_reporter which
# receive all the info
def custom_reporter(**kwargs):
    # send event to sentry
    capture_message(kwargs)
    # for discovering all the possible events go to  debian_watcher.change
