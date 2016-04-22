import logging
import time


__version__ = 0.1


def get_telemetry_uptake(uri, product, channel):
    pass


def is_ready(change, current_uptake=None):
    if change.type == "time":
        if time.now() > change.when:
            return True
    elif change.type == "uptake":
        if current_uptake >= change.telemetry_uptake:
            return True

    return False


def run_agent(balrog_api_root, balrog_username, balrog_password, telemetry_api_root, sleeptime=30):
    while True:
        logging.warning("doing stuff")
        time.sleep(sleeptime)
#    scheduled_change_client = ScheduledChangesAPI(balrog_api_root, balrog_api_auth)
#    telemetry_client = TelemetryClient(telemetry_api_root)
#
#    for change in scheduled_change_client.get_changes():
#        current_uptake = None
#        if change.type == "uptake":
#            current_uptake = telemetry_client.get_uptake(change.telemetry_product, change.telemetry_channel)
#        if is_ready(change):
#            scheduled_change_client.enact_change(change)


def main():
    import configargparse
    import daemonize
    import functools

    parser = configargparse.ArgParser(description="Balrog Agent", default_config_files=["balrog_agent.ini"])
    parser.add_argument("--balrog-api-root", required=True)
    parser.add_argument("--balrog-username", required=True)
    parser.add_argument("--balrog-password", required=True)
    parser.add_argument("-t", "--telemetry-api-root", required=True)

    args = parser.parse_args()

    runner = functools.partial(
        run_agent,
        args.balrog_api_root, args.balrog_username, args.balrog_password,
        args.telemetry_api_root
    )
    daemon = daemonize.Daemonize(app="balrog_agent", pid="balrog_agent.pid", action=runner, foreground=True)
    daemon.start()


if __name__ == "__main__":
    main()
