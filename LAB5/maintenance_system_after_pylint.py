"""Manage warehouse assets and their maintenance schedules."""

import json
import tempfile
from datetime import date, datetime, timedelta

assets = {}
SERVICE_INTERVAL_DAYS = 90


def register_asset(asset_id, machine_type, logs=None):
    """Register an asset and record its ID in the supplied log."""
    if not isinstance(asset_id, str) or not asset_id.strip():
        raise ValueError("Asset ID cannot be empty.")
    if logs is None:
        logs = []
    assets[asset_id] = {
        "type": machine_type,
        "last_service": date.today().isoformat(),
    }
    logs.append(asset_id)
    print("Registered", asset_id, "- total registrations this run:", len(logs))


def update_service_date(asset_id, service_date):
    """Update an asset's service date after validating the input."""
    if asset_id not in assets:
        print("Could not update", asset_id, "- asset not found")
        return
    try:
        parsed_date = datetime.strptime(service_date, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        print("Could not update", asset_id, "- invalid date")
        return
    assets[asset_id]["last_service"] = parsed_date.isoformat()


def due_for_inspection():
    """Return asset IDs whose last service exceeds the interval."""
    due = []
    today = date.today()
    for asset_id, asset in assets.items():
        last_service = datetime.strptime(asset["last_service"], "%Y-%m-%d").date()
        if today - last_service > timedelta(days=SERVICE_INTERVAL_DAYS):
            due.append(asset_id)
    return due


def change_interval(days):
    """Set a positive maintenance interval in days."""
    global SERVICE_INTERVAL_DAYS
    if not isinstance(days, int) or isinstance(days, bool) or days <= 0:
        raise ValueError("Service interval must be a positive integer.")
    SERVICE_INTERVAL_DAYS = days


def export_service_report(file="maintenance.json"):
    """Export the current asset records as formatted JSON."""
    with open(file, "w", encoding="utf-8") as report_file:
        json.dump(assets, report_file, indent=2)
    print("Report written to", file)


def write_scratch_copy():
    """Write a scratch JSON copy."""
    path = tempfile.mktemp(suffix=".json")
    with open(path, "w", encoding="utf-8") as scratch_file:
        json.dump(assets, scratch_file)
    print("Scratch copy at", path)


def print_alerts():
    """Print an alert for each asset overdue for inspection."""
    for asset_id in due_for_inspection():
        print("ALERT: inspection overdue for", asset_id, assets[asset_id]["type"])


def main():
    """Run the warehouse maintenance demonstration."""
    register_asset("FL-01", "Forklift")
    register_asset("CV-07", "Conveyor")
    register_asset("PJ-03", "Pallet Jack")
    register_asset("FL-01", "Crane")
    update_service_date("FL-01", "2025-01-15")
    update_service_date("XX-99", "2025-02-01")
    change_interval(90)
    service_date = input(
        "Last service date for CV-07 (YYYY-MM-DD, Enter to skip): "
    )
    if service_date:
        update_service_date("CV-07", service_date)
    if not assets:
        print("No assets registered.")
        return
    print_alerts()
    export_service_report()
    write_scratch_copy()


if __name__ == "__main__":
    main()
