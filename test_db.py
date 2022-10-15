from os import remove
from datetime import datetime
from db import Database


class Tests:

    def setup_method(self) -> None:
        self.test_db_filename = "test.db"
        self.database = Database(self.test_db_filename)
        self.database.initialize_database()
        self.date_format = "%Y-%m-%d"
        self.date_today = datetime.strptime("2022-10-10", self.date_format).date()
        self.next_periodicity_due_date = datetime.strptime("2022-10-11", self.date_format).date()
        self.dummy_name = "new habit"
        create_habit_status = self.database.create_habit(self.dummy_name, "a new one", 1, self.date_today,
                                                         self.next_periodicity_due_date, 0)
        assert create_habit_status is True

        create_event_status = self.database.create_event(1, True, self.date_today, 0)
        assert create_event_status is True

    def test_insert_habit(self) -> None:
        create_habit_status = self.database.create_habit("another habit", "a newer one", 1, self.date_today,
                                                         self.next_periodicity_due_date, 0)
        assert create_habit_status is True

    def test_insert_event(self) -> None:
        create_event_status = self.database.create_event(1, True, self.date_today, 0)
        assert create_event_status is True

    def test_select_id_by_name(self) -> None:
        assert self.database.read_habit_unique_id(self.dummy_name)[0] == 1

        assert self.database.read_habit_unique_id("unknown") is None

    def test_select_name_by_id(self) -> None:
        assert self.database.read_habit_name(1) is not None

        assert self.database.read_habit_name(12) is None

    def test_select_periodicity(self) -> None:
        assert self.database.read_habit_periodicity(1)[0] == 1

        assert self.database.read_habit_periodicity(12) is None

    def test_select_default_time(self) -> None:
        assert self.database.read_habit_default_time(1)[0] == 0

        assert self.database.read_habit_default_time(12) is None

    def test_select_next_periodicity_due_date(self) -> None:
        assert self.database.read_next_periodicity_due_date(1)[0] == "2022-10-11"

        assert self.database.read_next_periodicity_due_date(12) is None

    def test_select_get_habit_events(self) -> None:
        assert len(self.database.read_habit_events(1)) == 1

        assert len(self.database.read_habit_events(12)) == 0

    def test_update_next_periodicity_due_date(self) -> None:
        next_periodicity_due_date = datetime.strptime("2022-10-13", self.date_format).date()
        assert self.database.update_next_periodicity_due_date(1, next_periodicity_due_date) is True

    def test_analyse_get_all(self) -> None:
        assert len(self.database.read_habits_by_not_finished()) >= 1

    def test_analyse_get_same_periodicity(self) -> None:
        assert len(self.database.read_habits_by_periodicity(1)) >= 1

    def test_delete_habit_and_events(self) -> None:
        assert self.database.delete_habit_and_events(1) is True

    def teardown_method(self) -> None:
        self.database.close_connection()
        remove(self.test_db_filename)
