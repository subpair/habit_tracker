from random import choices, randrange
from habit import Habit
from os import remove


class Tests:

    def setup_method(self):
        """
        Steps:\n
        1: Set database filename \n
        2: Initialize habit objects \n
        3: Set Terminal clearing to off \n
        4: assign habit definitions \n
        5: create habits in the database
        """

        # 1 set db filename
        self.db_filename = "test.db"

        # 2 initialize habit objects
        self.habit_one = Habit(self.db_filename)
        self.habit_two = Habit(self.db_filename)
        self.habit_three = Habit(self.db_filename)
        self.habit_four = Habit(self.db_filename)
        self.habit_five = Habit(self.db_filename)

        # 3 set terminal clearing to off
        self.habit_one.helper_clear_terminal(False)
        self.habit_two.helper_clear_terminal(False)
        self.habit_three.helper_clear_terminal(False)
        self.habit_four.helper_clear_terminal(False)
        self.habit_five.helper_clear_terminal(False)

        # 4 assign habit definitions
        self.habit_one.name = "practice guitar"
        self.habit_one.description = "for at least 30min"
        self.habit_one.periodicity = "daily"
        self.habit_one.default_time_value = 30

        self.habit_two.name = "sleep 6 hours"
        self.habit_two.description = "at least 6 hours per day"
        self.habit_two.periodicity = "daily"
        self.habit_two.default_time_value = 360

        self.habit_three.name = "read a book"
        self.habit_three.description = "every week a little bit"
        self.habit_three.periodicity = "weekly"
        self.habit_three.default_time_value = 0

        self.habit_four.name = "do code challenges"
        self.habit_four.description = "at least 30 min"
        self.habit_four.periodicity = "daily"
        self.habit_four.default_time_value = 30

        self.habit_five.name = "study daily"
        self.habit_five.description = "without interruptions"
        self.habit_five.periodicity = "daily"
        self.habit_five.default_time_value = 120


        # 5 create habit records in the database
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

    def test_create_events(self):
        """
        Simulate events for 31 days
        """

        days = 31

        # simulating events
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

    def teardown_method(self):
        """
        Steps:\n
        1: Test the analyse functions\n
        2: Test the habit removal function\n
        3: Close connections to database \n
        4: Remove database file
        """

        # Test habit analyse functions
        self.habit_one.analyse("all")
        self.habit_one.analyse("all same periodicity", "daily")
        self.habit_one.analyse("all same periodicity", "weekly")
        self.habit_one.analyse("longest streak", self.habit_one.name)
        self.habit_one.analyse("longest streak", self.habit_two.name)
        self.habit_one.analyse("longest streak", self.habit_three.name)
        self.habit_one.analyse("longest streak", self.habit_four.name)
        self.habit_one.analyse("longest streak", self.habit_five.name)
        self.habit_one.analyse("longest streak of all")
        self.habit_one.analyse("time", self.habit_one.name)
        self.habit_one.analyse("time", self.habit_two.name)
        self.habit_one.analyse("time", self.habit_three.name)
        self.habit_one.analyse("time", self.habit_four.name)
        self.habit_one.analyse("time", self.habit_five.name)

        # 2 Test habit removal function
        self.habit_one.remove(self.habit_one.name, True)
        self.habit_two.remove(self.habit_two.name, True)
        self.habit_three.remove(self.habit_three.name, True)
        self.habit_four.remove(self.habit_four.name, True)
        self.habit_five.remove(self.habit_five.name, True)

        # 3 Close database connections
        self.habit_one.database.close_connection()
        self.habit_two.database.close_connection()
        self.habit_three.database.close_connection()
        self.habit_four.database.close_connection()
        self.habit_five.database.close_connection()

        # 3 Remove database file
        remove(self.db_filename)
