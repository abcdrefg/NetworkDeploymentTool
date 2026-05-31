"""Initialize the NetworkDeployment MongoDB database."""

import argparse
from datetime import datetime
from pathlib import Path

from werkzeug.security import generate_password_hash

from server.core.DatabaseConnection import DatabaseConnection

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin1"

COLLECTIONS = (
    DatabaseConnection.user_collection,
    DatabaseConnection.devices_collection,
    DatabaseConnection.commands_collection,
    DatabaseConnection.deployment_status,
    DatabaseConnection.config_versions,
    DatabaseConnection.unit_tests,
)

DEFAULT_DEPLOYMENT_STATUS = {
    "Deployed": "False",
    "SyntaxTest": "False",
    "UnitTest": "False",
    "AttachemendPoint": "",
    "ImageName": "sandbox-server",
    "SrvAddress": "10.0.0.2",
}


def seed_unit_tests(db: DatabaseConnection) -> int:
    testcases_dir = Path(__file__).resolve().parent.parent / "testcases"
    if not testcases_dir.is_dir():
        return 0

    collection = db.database_name[db.unit_tests]
    inserted = 0
    for test_file in sorted(testcases_dir.glob("*.py")):
        testname = test_file.name
        if collection.find_one({"testname": testname}) is not None:
            continue
        collection.insert_one({"testname": testname, "isActive": "false"})
        inserted += 1
    return inserted


def init_database(reset: bool = False) -> None:
    db = DatabaseConnection()
    database = db.database_name

    if reset:
        for collection_name in COLLECTIONS:
            database[collection_name].drop()
        print("Dropped existing collections.")

    users = database[db.user_collection]
    deployment_status = database[db.deployment_status]
    config_versions = database[db.config_versions]

    users.create_index("username", unique=True)

    for collection_name in (
        db.devices_collection,
        db.commands_collection,
    ):
        database[collection_name]

    if deployment_status.find_one() is None:
        initial_config = config_versions.insert_one(
            {"configs": {}, "timestamp": datetime.now()}
        )
        status = {**DEFAULT_DEPLOYMENT_STATUS, "CurrentConfig": initial_config.inserted_id}
        deployment_status.insert_one(status)
        print("Created DeploymentStatus and initial ConfigVersions record.")
    else:
        print("DeploymentStatus already exists, skipping.")

    existing_admin = users.find_one({"username": ADMIN_USERNAME})
    password_hash = generate_password_hash(ADMIN_PASSWORD)
    if existing_admin is None:
        users.insert_one({"username": ADMIN_USERNAME, "password": password_hash})
        print(f"Created admin user '{ADMIN_USERNAME}'.")
    else:
        users.update_one(
            {"username": ADMIN_USERNAME},
            {"$set": {"password": password_hash}},
        )
        print(f"Updated password for existing user '{ADMIN_USERNAME}'.")

    unit_tests_added = seed_unit_tests(db)
    if unit_tests_added:
        print(f"Registered {unit_tests_added} unit test(s) from testcases/.")

    print("Database initialization complete.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize the NetworkDeployment MongoDB database.")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Drop all collections before initializing.",
    )
    args = parser.parse_args()
    init_database(reset=args.reset)


if __name__ == "__main__":
    main()
