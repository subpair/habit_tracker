"""Unittest for habit module and general application features"""
from os import remove
from datetime import date, timedelta
from habit import Habit
from sample_data import SampleData


class TestProject:
    """Test class for project tests."""
    def setup_method(self) -> None:
        """
        Initialize a test habit and create one event for it.

        Afterwards initialize another habit object which is used in further tests.

        """
        self.test_db_filename: str = "test.db"
        self.habit = Habit("dummy object", db_filename=self.test_db_filename)
        self.habit.initialize_database()
        assert len(self.habit.database.read_database_structure()) == 3
        self.habit.description = "dummy for testing"
        self.habit.periodicity = 1
        self.habit.default_time = 30
        self.habit.generate_new_dates = False
        self.habit.manipulate_time(-31)
        self.habit.create_habit()
        self.habit.set_id(self.habit.name)
        self.habit.set_periodicity(self.habit.unique_id)
        self.habit.set_next_periodicity_due_date(self.habit.unique_id)
        self.habit.completed = True
        self.habit.create_event_update(self.habit.completed, self.habit.next_periodicity_due_date)
        self.habit_one = Habit("practice guitar", db_filename=self.test_db_filename)

    def test_dummy_exists_and_has_event(self) -> None:
        """Test if the dummy habit was created and has one event."""
        assert self.habit.is_existing(self.habit.name) is True
        assert self.habit.get_event_count(self.habit.unique_id) == 1

    def test_is_existing(self) -> None:
        """Look for a habit which does not exist"""
        assert self.habit.is_existing("unknown") is False

    def test_set_id(self) -> None:
        """Test the id assignment and if it is 0 when no record with a given name exists"""
        habit_name = "unknown"
        self.habit_unknown = Habit(habit_name, db_filename=self.test_db_filename)
        self.habit_unknown.set_id(habit_name)
        assert self.habit_unknown.unique_id == 0
        self.habit_unknown.database.close_connection()

        self.habit.set_id(self.habit.name)
        assert self.habit.unique_id == 1

    def test_set_properties(self) -> None:
        """
        Test the property assignments of periodicity, next_periodicity_due_date, default_time and name and if they have
        default values if there are no valid records for them.

        """
        habit_name = "unknown"
        self.habit_unknown = Habit(habit_name, db_filename=self.test_db_filename)
        self.habit_unknown.set_periodicity(self.habit_unknown.unique_id)
        self.habit_unknown.set_next_periodicity_due_date(self.habit_unknown.unique_id)
        self.habit_unknown.set_default_time(self.habit_unknown.unique_id)
        self.habit_unknown.set_name(self.habit_unknown.unique_id)
        assert self.habit_unknown.periodicity == 0
        assert self.habit_unknown.next_periodicity_due_date == date.today()
        assert self.habit_unknown.default_time == 0
        assert self.habit_unknown.name == "unknown"
        self.habit_unknown.database.close_connection()

        self.habit.set_periodicity(self.habit.unique_id)
        assert self.habit.periodicity == 1

        self.habit.set_next_periodicity_due_date(self.habit.unique_id)
        # Because there is already one event, the next periodicity due date will be 2 days later instead of 1
        next_date = False
        if self.habit.next_periodicity_due_date == self.habit.date_today + timedelta(days=2 * self.habit.periodicity):
            next_date = True
        assert next_date is True

        self.habit.set_default_time(self.habit.unique_id)
        assert self.habit.default_time == 30

    def test_create_habit(self) -> None:
        """Test the creation of a new habit."""
        self.habit_one.description = "for at least 30min"
        self.habit_one.periodicity = 1
        self.habit_one.default_time = 30
        self.habit_one.generate_new_dates = True
        self.habit_one.create_habit()
        assert self.habit_one.is_existing(self.habit_one.name) is True

    def test_create_event_simple(self) -> None:
        """Test the creation of another event by using the simple event update function."""
        self.habit.create_event_update(True, self.habit.next_periodicity_due_date)

        assert self.habit.get_event_count(self.habit.unique_id) == 2

    def test_create_delayed_event(self) -> None:
        """Test the creation of another event by using the event logic function and if the fills are correct."""
        self.habit.manipulate_time(+7)
        self.habit.create_event(self.habit.name, self.habit.next_periodicity_due_date)

        assert self.habit.get_event_count(self.habit.unique_id) == 7

    def test_analyse(self) -> None:
        """Test the analyse function and if they all put out the existing event and the correct detail for this."""
        assert len(self.habit.analyse_all_active()) == 1
        assert len(self.habit.analyse_all_active_same_periodicity(1)) == 1
        assert self.habit.analyse_longest_streak() == (1, 1)
        assert self.habit.analyse_longest_streak(self.habit.unique_id) == (1, 1)
        assert self.habit.analyse_time(self.habit.unique_id) == 30

    def test_delete_habit(self) -> None:
        """Test the deletion of a habit and if the record is not existing anymore."""
        self.habit.delete(self.habit.unique_id)
        assert self.habit.is_existing(self.habit.name) is False

    def test_sample_data(self):
        """Test the sample data and if all 5 sample habits are created and their event data is inserted."""
        samples = SampleData(31, "test.db")
        samples.create_habits()
        samples.simulate_events()
        # There will be 6 events as we have the dummy from this test also
        assert len(samples.habit_one.database.read_habits()) == 5 + 1
        # There should be at-least 6 entries. (the real value with current weights is around ~120)
        assert len(samples.habit_one.database.read_events()) > 5 + 1
        samples.closing_connections()

    def teardown_method(self) -> None:
        """Close the database connections and remove the database file"""
        self.habit.database.close_connection()
        self.habit_one.database.close_connection()
        remove(self.test_db_filename)
