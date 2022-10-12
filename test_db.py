from db import Database
from os import remove
from datetime import datetime


class Tests:

    def setup_method(self):
        self.db_filename = "test.db"
        self.database = Database(self.db_filename)
        self.database.initialize_database()
        self.date_format = "%Y-%m-%d"
        self.date_today = datetime.strptime("2022-10-10", self.date_format).date()
        self.next_periodicity_due_date = datetime.strptime("2022-10-11", self.date_format).date()
        self.dummy_name = "new habit"
        insert_habit_status = self.database.insert_habit(self.dummy_name, "a new one", 1, self.date_today,
                                                         self.next_periodicity_due_date, 0)
        assert insert_habit_status is True

        insert_event_status = self.database.insert_event(1, True, self.date_today, 0)
        assert insert_event_status is True

    def test_insert_habit(self):
        insert_habit_status = self.database.insert_habit("another habit", "a newer one", 1, self.date_today,
                                                         self.next_periodicity_due_date, 0)
        assert insert_habit_status is True

    def test_insert_event(self):
        insert_event_status = self.database.insert_event(1, True, self.date_today, 0)
        assert insert_event_status is True

    def test_select_id_by_name(self):
        assert self.database.select_get_habit_unique_id(self.dummy_name)[0] == 1

        assert self.database.select_get_habit_unique_id("unknown") is None

    def test_select_name_by_id(self):
        assert self.database.select_get_habit_name(1) is not None

        assert self.database.select_get_habit_name(12) is None

    def test_select_periodicity(self):
        assert self.database.select_periodicity(1)[0] == 1

        assert self.database.select_periodicity(12) is None

    def test_select_default_time(self):
        assert self.database.select_get_habit_default_time(1)[0] == 0

        assert self.database.select_get_habit_default_time(12) is None

    def test_select_next_periodicity_due_date(self):
        assert self.database.select_next_periodicity_due_date(1)[0] == "2022-10-11"

        assert self.database.select_next_periodicity_due_date(12) is None

    def test_select_get_habit_events(self):
        assert len(self.database.select_get_habit_events(1)) == 1

        assert len(self.database.select_get_habit_events(12)) == 0

    def test_update_next_periodicity_due_date(self):
        next_periodicity_due_date = datetime.strptime("2022-10-13", self.date_format).date()
        assert self.database.update_next_periodicity_due_date(1, next_periodicity_due_date) is True

    def test_analyse_get_all(self):
        assert len(self.database.analyse_get_all()) >= 1

    def test_analyse_get_same_periodicity(self):
        assert len(self.database.analyse_get_same_periodicity(1)) >= 1

    def test_delete_habit_and_events(self):
        assert self.database.delete_habit_and_events(1) is True

    def teardown_method(self):
        self.database.close_connection()
        remove(self.db_filename)
