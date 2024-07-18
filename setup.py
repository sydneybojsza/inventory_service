import os
import subprocess
from setuptools import setup, find_packages, Command


def set_python_path():
    """Appends the app directory to the Python path (works on Win & Linux)"""
    if os.name == "nt":
        os.environ["PYTHONPATH"] = f"{os.environ['PYTHONPATH']};{os.getcwd()}\\app"
    elif os.name == "posix":
        os.environ["PYTHONPATH"] = f"{os.getcwd()}/app"


class SetupDatabase(Command):
    """A custom command to setup the database."""

    description = "setup the database by creating necessary tables"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run database setup script."""
        set_python_path()
        subprocess.check_call(
            [
                "python",
                "-c",
                "from app.db import engine; from app.models import Base; Base.metadata.create_all(bind=engine)",
            ]
        )


class PopulateDatabase(Command):
    """A custom command to populate the database with dummy data."""

    description = "populate the database with dummy data"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run script to populate the database with dummy data."""
        from app.db import SessionLocal
        from app.models import User, InventoryItem

        db = SessionLocal()
        try:
            # Add dummy users
            user1 = User(id="testuser1", password="fakehashedpassword1")
            user2 = User(id="testuser2", password="fakehashedpassword2")
            db.add(user1)
            db.add(user2)

            # Add dummy inventory items for user1
            item1 = InventoryItem(user_id="testuser1", item_name="sword", quantity=2)
            item2 = InventoryItem(user_id="testuser1", item_name="shield", quantity=1)

            # Add dummy inventory items for user2
            item3 = InventoryItem(user_id="testuser2", item_name="potion", quantity=5)
            item4 = InventoryItem(user_id="testuser2", item_name="bow", quantity=1)

            db.add(item1)
            db.add(item2)
            db.add(item3)
            db.add(item4)
            db.commit()
        finally:
            db.close()


class TestCommand(Command):
    """A custom command to run tests."""

    description = "run tests with pytest"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run the tests."""
        set_python_path()
        subprocess.check_call(["pytest", "-vv"])


setup(
    name="inventory_service",
    version="0.1.0",
    packages=find_packages(where="app"),
    package_dir={"": "app"},
    install_requires=["fastapi", "uvicorn", "sqlalchemy", "pydantic", "pytest"],
    cmdclass={
        "setup_db": SetupDatabase,
        "test": TestCommand,
        "populate_db": PopulateDatabase,
    },
)
