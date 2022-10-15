"""
Unittest for database
"""
from os import remove
from datetime import datetime
from db import Database


class TestDatabase:
    """
    Test class for database tests.
    """
    def setup_method(self) -> None:
        """
        Initialize the database and inserts one test dummy habit with one event into the database for further tests.
        """
        self.test_db_filename = "test.db"
        self.database = Database(self.test_db_filename)
        self.database.initialize_database()
        assert len(self.database.read_database_structure()) == 3
        self.date_format = "%Y-%m-%d"
        self.date_today = datetime.strptime("2022-10-10", self.date_format).date()
        self.next_periodicity_due_date = datetime.strptime("2022-10-11", self.date_format).date()
        self.dummy_name = "new habit"

        create_habit_status = self.database.create_new_habit(self.dummy_name, "a new one", 1, self.date_today,
                                                             self.next_periodicity_due_date, 0)
        assert create_habit_status is True

        create_event_status = self.database.create_new_event(1, True, self.date_today, 0)
        assert create_event_status is True

    def test_connection(self) -> None:
        """
        Test the database connection by disconnecting and using a command. Afterwards manually connect again and try the
        same
        """
        self.database.close_connection()
        assert len(self.database.read_database_structure()) == 0
        self.database.open_connection()
        assert len(self.database.read_database_structure()) == 3
        self.database.close_connection()

    def test_create_habit(self) -> None:
        """
        Test the creation of a habit record
        """
        create_habit_status = self.database.create_new_habit("another habit", "a newer one", 1, self.date_today,
                                                             self.next_periodicity_due_date, 0)
        assert create_habit_status is True

    def test_create_event(self) -> None:
        """
        Test the creation of a habit event record
        """
        create_event_status = self.database.create_new_event(1, True, self.date_today, 0)
        assert create_event_status is True

    def test_read_habit_unique_id(self) -> None:
        """
        Test reading the id of the test dummy habit
        """
        assert self.database.read_habit_unique_id(self.dummy_name)[0] == 1
        assert self.database.read_habit_unique_id("unknown") is None

    def test_read_habits_unique_ids(self) -> None:
        """
        Test reading all ids and checking of one record is found
        """
        assert len(self.database.read_habits_unique_ids()) == 1

    def test_read_name_by_id(self) -> None:
        """
        Test reading name by id and if a record is found for a valid and if None is returned for a non-existing record
        """
        assert self.database.read_habit_name(1) is not None
        assert self.database.read_habit_name(12) is None

    def test_read_periodicity(self) -> None:
        """
        Test reading the periodicity of a habit and if None is returned for a non-existing record
        """
        assert self.database.read_habit_periodicity(1)[0] == 1
        assert self.database.read_habit_periodicity(12) is None

    def test_read_default_time(self) -> None:
        """
        Test reading the default time of a habit and if None is returned for a non-existing record
        """
        assert self.database.read_habit_default_time(1)[0] == 0
        assert self.database.read_habit_default_time(12) is None

    def test_read_next_periodicity_due_date(self) -> None:
        """
        Test reading the next periodicity due date of a habit and if None is returned for a non-existing record
        """
        assert self.database.read_next_periodicity_due_date(1)[0] == "2022-10-11"
        assert self.database.read_next_periodicity_due_date(12) is None

    def test_read_habit_events(self) -> None:
        """
        Test reading all events for a specific habit id and if 0 is returned for a non-existing record
        """
        assert len(self.database.read_habit_events(1)) == 1
        assert len(self.database.read_habit_events(12)) == 0

    def test_update_next_periodicity_due_date(self) -> None:
        """
        Test updating the next periodicity due date of an existing record
        """
        next_periodicity_due_date = datetime.strptime("2022-10-13", self.date_format).date()
        assert self.database.update_next_periodicity_due_date(1, next_periodicity_due_date) is True

    def test_analyse_get_all(self) -> None:
        """
        Test reading all habits with the status finished False
        """
        assert len(self.database.read_habits_by_not_finished()) >= 1

    def test_analyse_get_same_periodicity(self) -> None:
        """
        Test reading all habits with the periodicity 0 (="daily")
        """
        assert len(self.database.read_habits_by_periodicity(1)) >= 1

    def test_delete_habit_and_events(self) -> None:
        """
        Test deleting a record and if the record is not existing anymore
        """
        assert self.database.delete_habit_and_events(1) is True
        assert len(self.database.read_habits()) == 0

    def teardown_method(self) -> None:
        """
        Close the database connection and remove the database file
        """
        self.database.close_connection()
        remove(self.test_db_filename)
