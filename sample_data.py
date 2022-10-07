from random import choices, randrange
from habit import Habit


class SampleData:
    def __init__(self, duration: int):
        """
        Initialize the sampledata object with a duration value for which the simulated events take place \n
        Steps:\n
        1: Set the database filename\n
        2: Initialize 5 predefined habits\n
        :param duration: time in days of which the sample data is offset
        """

        self.duration = duration
        # 1 set database filename
        self.db_filename = "sample.db"

        # 2 initialize habit objects
        self.habit_one = Habit(self.db_filename)
        self.habit_two = Habit(self.db_filename)
        self.habit_three = Habit(self.db_filename)
        self.habit_four = Habit(self.db_filename)
        self.habit_five = Habit(self.db_filename)

    def create_habits(self):
        """
        Steps:\n
        1: Set the values name, description, periodicity and default_time_value for the 5 predefined habits \n
        2: Negate the duration value of the simulation, so the sample data becomes usable today\n
        3: Store the habits in the database
        """

        # 1 assigning the habit definitions and manipulating the time value
        self.habit_one.name = "practice guitar"
        self.habit_one.description = "for at least 30min"
        self.habit_one.periodicity = "daily"
        self.habit_one.default_time_value = 30
        self.habit_one.manipulate_time(-self.duration)

        self.habit_two.name = "sleep 6 hours"
        self.habit_two.description = "at least 6 hours per day"
        self.habit_two.periodicity = "daily"
        self.habit_two.default_time_value = 360
        self.habit_two.manipulate_time(-self.duration)

        self.habit_three.name = "read a book"
        self.habit_three.description = "every week a little bit"
        self.habit_three.periodicity = "weekly"
        self.habit_three.default_time_value = 0
        self.habit_three.manipulate_time(-self.duration)

        self.habit_four.name = "do code challenges"
        self.habit_four.description = "at least 30 min"
        self.habit_four.periodicity = "daily"
        self.habit_four.default_time_value = 30
        self.habit_four.manipulate_time(-self.duration)

        self.habit_five.name = "study daily"
        self.habit_five.description = "without interruptions"
        self.habit_five.periodicity = "daily"
        self.habit_five.default_time_value = 120
        self.habit_five.manipulate_time(-self.duration)

        # 2 storing the habits in the database
        self.habit_one.create(self.habit_one.name, self.habit_one.description, self.habit_one.periodicity,
                              self.habit_one.default_time_value)

        self.habit_two.create(self.habit_two.name, self.habit_two.description, self.habit_two.periodicity,
                              self.habit_two.default_time_value)

        self.habit_three.create(self.habit_three.name, self.habit_three.description, self.habit_three.periodicity,
                                self.habit_three.default_time_value)
        self.habit_four.create(self.habit_four.name, self.habit_four.description, self.habit_four.periodicity,
                               self.habit_four.default_time_value)

        self.habit_five.create(self.habit_five.name, self.habit_five.description, self.habit_five.periodicity,
                               self.habit_five.default_time_value)

    def simulate_events(self):
        """
        Simulate the 5 defined habits events by putting in random values with different weights \n
        completed can be either true or false \n
        time_invested is optional and passed as 0 when not used or a defined range \n
        also  simulates a skip of the habit e.g. when the user forgot to check the habit
        """

        # "practice guitar"
        days = self.duration
        print("simulating events for {days} days".format(days=days))
        for i in range(days):
            self.habit_one.manipulate_time(+1)
            answers = [True, False]
            completion = choices(answers, weights=(25, 75))[0]
            use_time = choices(answers, weights=(90, 10))[0]
            if use_time:
                time_invested = randrange(0, 240)
            else:
                time_invested = 0
            skip_habit = choices(answers, weights=(50, 50))[0]
            if not skip_habit:
                self.habit_one.event(self.habit_one.name, completion, time_invested)
            else:
                print("skipping")

        # "sleep 6 hours"
        days = self.duration
        print("simulating events for {days} days".format(days=days))
        for i in range(days):
            self.habit_two.manipulate_time(+1)
            answers = [True, False]
            completion = choices(answers, weights=(95, 5))[0]
            use_time = choices(answers, weights=(25, 75))[0]
            if use_time:
                time_invested = randrange(0, 720)
            else:
                time_invested = 0
            skip_habit = choices(answers, weights=(2, 98))[0]
            if not skip_habit:
                self.habit_two.event(self.habit_two.name, completion, time_invested)
            else:
                print("skipping")

        # "read a book"
        days = self.duration
        print("simulating events for {days} days".format(days=days))
        for i in range(days):
            self.habit_three.manipulate_time(+1)
            answers = [True, False]
            completion = choices(answers, weights=(10, 90))[0]
            use_time = choices(answers, weights=(25, 75))[0]
            if use_time:
                time_invested = randrange(0, 120)
            else:
                time_invested = 0
            skip_habit = choices(answers, weights=(90, 10))[0]
            if not skip_habit:
                self.habit_three.event(self.habit_three.name, completion, time_invested)
            else:
                print("skipping")

        # "do code challenges"
        days = self.duration
        print("simulating events for {days} days".format(days=days))
        for i in range(days):
            self.habit_four.manipulate_time(+1)
            answers = [True, False]
            completion = choices(answers, weights=(75, 25))[0]
            use_time = choices(answers, weights=(75, 25))[0]
            if use_time:
                time_invested = randrange(0, 180)
            else:
                time_invested = 0
            skip_habit = choices(answers, weights=(40, 60))[0]
            if not skip_habit:
                self.habit_four.event(self.habit_four.name, completion, time_invested)
            else:
                print("skipping")

        # "study daily"
        days = self.duration
        print("simulating events for {days} days".format(days=days))
        for i in range(days):
            self.habit_five.manipulate_time(+1)
            answers = [True, False]
            completion = choices(answers, weights=(99, 1))[0]
            use_time = choices(answers, weights=(95, 5))[0]
            if use_time:
                time_invested = randrange(120, 480)
            else:
                time_invested = 0
            skip_habit = choices(answers, weights=(1, 99))[0]
            if not skip_habit:
                self.habit_five.event(self.habit_five.name, completion, time_invested)
            else:
                print("skipping")

    def closing_connections(self):
        """
        Close the database connections to avoid file locks
        """

        self.habit_one.database.close_connection()
        self.habit_two.database.close_connection()
        self.habit_three.database.close_connection()
        self.habit_four.database.close_connection()
        self.habit_five.database.close_connection()


