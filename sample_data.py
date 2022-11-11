"""Contains a sample data generator."""
from typing import Optional
from random import choices, randrange
from habit import Habit


class SampleData:
    """SampleData class for generating random events."""

    def __init__(self, duration: int, db_filename: Optional[str] = None) -> None:
        """
        Initialize the sampledata object with a duration value for which the simulated events take place.

        Steps:

        1: Set the database filename and initialize the sample database

        2: Initialize 5 predefined habits

        :param duration: int time in days of which the sample data is offset
        """
        self.duration: int = duration
        # 1 Set the database filename and initialize the sample database
        if db_filename is None:
            self.db_filename: str = "sample.db"
        else:
            self.db_filename = db_filename
        self.habit_sample = Habit(db_filename=self.db_filename)
        self.habit_sample.initialize_database()
        self.habit_sample.database.close_connection()

        # 2 initialize habit objects
        self.habit_one = Habit(db_filename=self.db_filename)
        self.habit_two = Habit(db_filename=self.db_filename)
        self.habit_three = Habit(db_filename=self.db_filename)
        self.habit_four = Habit(db_filename=self.db_filename)
        self.habit_five = Habit(db_filename=self.db_filename)

    def create_habits(self) -> None:
        """
        Create 5 habits with predefined properties.

        Steps

        1: Set the values name, description, periodicity, default_time_value and user_mode for the 5 predefined habits
        and negate the duration value of the simulation, so the sample data becomes usable today.

        2: Store the habits in the database

        """
        # 1 assigning the habit definitions and manipulating the time value
        self.habit_one.name = "practice guitar"
        self.habit_one.description = "for at least 30min"
        self.habit_one.periodicity = 1
        self.habit_one.default_time = 30
        self.habit_one.generate_new_dates = False
        self.habit_one.manipulate_time(-self.duration)

        self.habit_two.name = "sleep 6 hours"
        self.habit_two.description = "at least 6 hours per day"
        self.habit_two.periodicity = 1
        self.habit_two.default_time = 360
        self.habit_two.generate_new_dates = False
        self.habit_two.manipulate_time(-self.duration)

        self.habit_three.name = "read a book"
        self.habit_three.description = "every week a little bit"
        self.habit_three.periodicity = 7
        self.habit_three.default_time = 0
        self.habit_three.generate_new_dates = False
        self.habit_three.manipulate_time(-self.duration)

        self.habit_four.name = "do code challenges"
        self.habit_four.description = "at least 30 min"
        self.habit_four.periodicity = 1
        self.habit_four.default_time = 30
        self.habit_four.generate_new_dates = False
        self.habit_four.manipulate_time(-self.duration)

        self.habit_five.name = "study daily"
        self.habit_five.description = "without interruptions"
        self.habit_five.periodicity = 1
        self.habit_five.default_time = 120
        self.habit_five.generate_new_dates = False
        self.habit_five.manipulate_time(-self.duration)

        # 2 storing the habits in the database
        self.habit_one.create_habit()
        self.habit_two.create_habit()
        self.habit_three.create_habit()
        self.habit_four.create_habit()
        self.habit_five.create_habit()

    def simulate_events(self) -> None:
        """
        Simulate the 5 defined habits events by putting in random values with different weights.

        completed can be either true or false

        time_invested is optional and passed as 0 when not used or a value from the defined range

        also simulates a skip of the habit e.g. when the user forgot to check the habit

        """
        # "practice guitar"
        days = self.duration
        for i in range(days):
            self.habit_one.manipulate_time(+1)
            answers = [True, False]
            self.habit_one.completed = choices(answers, weights=(50, 50))[0]
            use_time = choices(answers, weights=(90, 10))[0]
            if use_time:
                self.habit_one.time = randrange(0, 240)
            else:
                self.habit_one.time = 0
            skip_habit = choices(answers, weights=(50, 50))[0]
            if not skip_habit:
                self.habit_one.set_id(self.habit_one.name)
                self.habit_one.set_next_periodicity_due_date(self.habit_one.unique_id)
                self.habit_one.create_event(self.habit_one.name, self.habit_one.next_periodicity_due_date)

        # "sleep 6 hours"
        days = self.duration
        for i in range(days):
            self.habit_two.manipulate_time(+1)
            answers = [True, False]
            self.habit_two.completed = choices(answers, weights=(95, 5))[0]
            use_time = choices(answers, weights=(25, 75))[0]
            if use_time:
                self.habit_two.time = randrange(0, 720)
            else:
                self.habit_two.time = 0
            skip_habit = choices(answers, weights=(1, 99))[0]
            if not skip_habit:
                self.habit_two.set_id(self.habit_two.name)
                self.habit_two.set_next_periodicity_due_date(self.habit_two.unique_id)
                self.habit_two.create_event(self.habit_two.name, self.habit_two.next_periodicity_due_date)

        # "read a book"
        days = self.duration
        for i in range(days):
            self.habit_three.manipulate_time(+1)
            answers = [True, False]
            self.habit_three.completed = choices(answers, weights=(30, 70))[0]
            use_time = choices(answers, weights=(75, 25))[0]
            if use_time:
                self.habit_three.time = randrange(0, 120)
            else:
                self.habit_three.time = 0
            skip_habit = choices(answers, weights=(5, 95))[0]
            if not skip_habit:
                self.habit_three.set_id(self.habit_three.name)
                self.habit_three.set_next_periodicity_due_date(self.habit_three.unique_id)
                self.habit_three.create_event(self.habit_three.name, self.habit_three.next_periodicity_due_date)

        # "do code challenges"
        days = self.duration
        for i in range(days):
            self.habit_four.manipulate_time(+1)
            answers = [True, False]
            self.habit_four.completed = choices(answers, weights=(75, 25))[0]
            use_time = choices(answers, weights=(75, 25))[0]
            if use_time:
                self.habit_four.time = randrange(0, 180)
            else:
                self.habit_four.time = 0
            skip_habit = choices(answers, weights=(40, 60))[0]
            if not skip_habit:
                self.habit_four.set_id(self.habit_four.name)
                self.habit_four.set_next_periodicity_due_date(self.habit_four.unique_id)
                self.habit_four.create_event(self.habit_four.name, self.habit_four.next_periodicity_due_date)

        # "study daily"
        days = self.duration
        for i in range(days):
            self.habit_five.manipulate_time(+1)
            answers = [True, False]
            self.habit_five.completed = choices(answers, weights=(99, 1))[0]
            use_time = choices(answers, weights=(95, 5))[0]
            if use_time:
                self.habit_five.time = randrange(120, 480)
            else:
                self.habit_five.time = 0
            skip_habit = choices(answers, weights=(1, 99))[0]
            if not skip_habit:
                self.habit_five.set_id(self.habit_five.name)
                self.habit_five.set_next_periodicity_due_date(self.habit_five.unique_id)
                self.habit_five.create_event(self.habit_five.name, self.habit_five.next_periodicity_due_date)

    def closing_connections(self) -> None:
        """Close the database connections to avoid a file lock."""
        self.habit_one.database.close_connection()
        self.habit_two.database.close_connection()
        self.habit_three.database.close_connection()
        self.habit_four.database.close_connection()
        self.habit_five.database.close_connection()
