from random import choices, randrange
from habit import Habit
from os import remove


class Tests:

    def setup_method(self):
        self.db_filename = "test.db"
        self.habit = Habit("dummy object", db_filename=self.db_filename)
        self.habit.database.initialize_database()
        self.habit.description = "dummy for testing"
        self.habit.periodicity = 1
        self.habit.default_time = 30
        self.habit.user_mode = False
        self.habit.manipulate_time(-31)
        self.test_dummy_create_status = self.habit.create_habit()

        self.habit.set_id(self.habit.name)
        self.habit.set_next_periodicity_due_date(self.habit.unique_id)
        self.habit.set_default_time(self.habit.unique_id)
        self.habit.set_periodicity(self.habit.unique_id)
        self.habit.create_event(True, self.habit.next_periodicity_due_date)

        self.habit_one = Habit("practice guitar", db_filename=self.db_filename)

    def test_dummy_exists_and_has_event(self):
        assert self.habit.is_existing(self.habit.name) is True
        assert self.habit.get_event_count(self.habit.unique_id) == 1

    def test_create_habit(self):
        self.habit_one.description = "for at least 30min"
        self.habit_one.periodicity = 1
        self.habit_one.default_time_value = 30
        self.habit_one.user_mode = True
        self.habit_one.create_habit()
        assert self.habit_one.is_existing(self.habit_one.name) is True

    def test_is_existing(self):
        """
        Look for a habit that was not created yet
        """
        assert self.habit.is_existing("unknown") is False

    def test_create_event(self):
        self.habit.set_id(self.habit.name)
        self.habit.set_next_periodicity_due_date(self.habit.unique_id)
        self.habit.set_default_time(self.habit.unique_id)
        self.habit.set_periodicity(self.habit.unique_id)
        self.habit.create_event(True, self.habit.next_periodicity_due_date)

        assert self.habit.get_event_count(self.habit.unique_id) == 2

    def test_create_delayed_event(self):
        self.habit.manipulate_time(+7)
        self.habit.set_id(self.habit.name)
        self.habit.set_next_periodicity_due_date(self.habit.unique_id)
        self.habit.set_default_time(self.habit.unique_id)
        self.habit.set_periodicity(self.habit.unique_id)
        self.habit.create_event_logic(True, self.habit.next_periodicity_due_date)

        assert self.habit.get_event_count(self.habit.unique_id) == 7

    def test_analytics(self):

        assert len(self.habit.analyse_all_active()) == 1
        assert len(self.habit.analyse_all_active_same_periodicity(1)) == 1
        assert self.habit.analyse_longest_streak() == (1, 1)
        assert self.habit.analyse_longest_streak(self.habit.unique_id) == (1, 1)
        assert self.habit.analyse_time(self.habit.unique_id) == 30

    def test_remove_habit(self):
        self.habit.remove(self.habit.unique_id)
        assert self.habit.is_existing(self.habit.name) is False

    def teardown_method(self):
        self.habit.database.close_connection()
        self.habit_one.database.close_connection()
        remove(self.db_filename)
