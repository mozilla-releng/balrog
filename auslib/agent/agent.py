def get_telemetry_uptake(uri, product, channel):
    pass


def is_ready(change, current_uptake=None):
    if change.type == "time":
        if time.now() > change.when:
            return True
    elif change.type == "uptake":
        if current_uptake >= change.telemetry_uptake
            return True

    return False


def run_agent(balrog_api_root, balrog_api_auth, telemetry_api_root, sleeptime=30):
    scheduled_change_client = ScheduledChangesAPI(balrog_api_root, balrog_api_auth)
    telemetry_client = TelemetryClient(telemetry_api_root)

    for change in scheduled_change_client.get_changes():
        current_uptake = None
        if change.type == "uptake":
            current_uptake = telemetry_client.get_uptake(change.telemetry_product, change.telemetry_channel)
        if is_ready(change):
            scheduled_change_client.enact_change(change)
