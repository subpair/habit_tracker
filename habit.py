from db import Database
from datetime import date, timedelta, datetime


class Habit:
    def __init__(self, name: str, description: str = None, periodicity: int = None, default_time: int = None,
                 db_filename: str = None, user_mode: bool = None):

        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.date_today = date.today()
        self.unique_id = 0
        self.next_periodicity_due_date = date.today()
        self.next_periodicity_range_start = date.today()
        self.date_format = "%Y-%m-%d"
        if default_time is None:
            self.default_time = 0
        else:
            self.default_time = default_time

        self.time = 0

        if db_filename is None:
            self.db_filename = "main.db"
        else:
            self.db_filename = db_filename
        self.database = Database(self.db_filename)

        if user_mode is None:
            self.user_mode = True
        else:
            self.user_mode = user_mode

    def initialize_database(self):
        self.database.initialize_database()

    def is_existing(self, habit_name: str):
        if self.database.select_get_habit_unique_id(habit_name) is not None:
            return True
        else:
            return False

    def set_id(self, habit_name: str):
        self.unique_id = self.database.select_get_habit_unique_id(habit_name)[0]

    def set_periodicity(self, habit_id: int):
        self.periodicity = self.database.select_periodicity(habit_id)[0]

    def set_next_periodicity_due_date(self, habit_id: int):
        next_periodicity_due_date = self.database.select_next_periodicity_due_date(habit_id)[0]
        self.next_periodicity_due_date = datetime.strptime(next_periodicity_due_date, self.date_format).date()

    def set_default_time(self, habit_id: int):
        self.default_time = self.database.select_get_habit_default_time(habit_id)[0]

    def create_habit(self, created_date: date = None, next_periodicity_due_date: date = None):
        if created_date is None:
            if self.user_mode:
                created_date = date.today()
            else:
                created_date = self.date_today
        if next_periodicity_due_date is None:
            next_periodicity_due_date = created_date + timedelta(days=self.periodicity)
        self.database.insert_habit(self.name, self.description, self.periodicity,
                                   created_date, next_periodicity_due_date, self.default_time)
        self.set_id(self.name)

    def create_event(self, completed: bool, next_periodicity_due_date: date, change_date: date = None,
                     time: int = None):
        if change_date is None:
            if self.user_mode:
                change_date = date.today()
            else:
                change_date = self.date_today
        if not completed:
            time = 0
        if time is None:
            time = self.default_time
        self.database.insert_event(self.unique_id, completed, change_date, time)
        self.next_periodicity_due_date = next_periodicity_due_date + timedelta(days=self.periodicity)
        self.database.update_next_periodicity_due_date(self.unique_id, self.next_periodicity_due_date)

    def create_event_logic(self, completed: bool, next_periodicity_due_date: date, change_date: date = None):
        if change_date is None:
            if self.user_mode:
                change_date = date.today()
            else:
                change_date = self.date_today

        update_lower_range = next_periodicity_due_date - timedelta(days=self.periodicity)
        if (change_date >= update_lower_range) and (change_date <= next_periodicity_due_date):
            self.create_event(completed, self.next_periodicity_due_date, change_date=change_date)
        elif change_date < update_lower_range:
            return False
        elif change_date > next_periodicity_due_date:
            update_lower_range, missed_dates = self.create_event_fill(update_lower_range)
            self.create_event(completed, self.next_periodicity_due_date, update_lower_range)
            return missed_dates

    def create_event_fill(self, update_lower_range: date):
        missed = int(((self.date_today - timedelta(days=self.periodicity)) - update_lower_range)
                     / timedelta(days=self.periodicity))
        missed_dates = {}
        for i in range(missed):
            missed_dates[i+1] = str(update_lower_range)
            self.create_event(False, self.next_periodicity_due_date, update_lower_range)
            self.database.update_next_periodicity_due_date(self.unique_id, self.next_periodicity_due_date)
            update_lower_range = self.next_periodicity_due_date - timedelta(days=self.periodicity)
        return update_lower_range, missed_dates

    def remove(self, habit_id: int):
        self.database.delete_habit_and_events(habit_id)

    def analyse(self, option: str):
        """
        The analyse-function will use the data from the database and give the user information about the existing data
        of the habits.\n
        :param option: can be "all", "all same periodicity", "longest streak of all", "longest streak" or "time"
        :return: always True
        """
        # "Show all currently tracked habits"
        if option == "all":
            self.analyse_all_active()
        # "Show all habits with the same periodicity"
        elif option == "all same periodicity":
            self.analyse_all_active_same_periodicity(self.periodicity)
        # "Return the longest run streak of all defined habits"
        elif option == "longest streak of all":
            self.analyse_longest_streak()
        # "Return the longest run streak for a given habit"
        elif option == "longest streak":
            self.analyse_longest_streak(self.unique_id)
        # "Return the longest run streak for a given habit"
        elif option == "time":
            self.analyse_time(self.unique_id)

    def analyse_all_active(self):
        result = self.database.analyse_get_all()
        return result

    def analyse_all_active_same_periodicity(self, periodicity: int):
        result = self.database.analyse_get_same_periodicity(periodicity)
        return result

    def analyse_longest_streak(self, habit_id: int = None):
        if habit_id is None:
            habit_unique_ids = self.database.select_get_all_habits_unique_ids()
        else:
            habit_unique_ids = [(habit_id,)]
        if habit_unique_ids:
            # Count the number of times an event was successful for a habit by iterating over all events in all
            # existing habits.
            highest_count_overall = 0
            highest_habit_id = 0
            for i in habit_unique_ids:
                all_events = self.database.select_get_habit_events(unique_id=i[0])
                count = 0
                highest_count = 0
                for j in all_events:
                    if j[2] == 1:
                        count += 1
                    # If a failure event was found the counter resets.
                    else:
                        count = 0
                    # If the current count is higher than the highest count for this habit, set it as the new highest
                    # count.
                    if count > highest_count:
                        highest_count = count
                # If the highest count is bigger than the overall highest count, save this and the habit id.
                if highest_count > highest_count_overall:
                    highest_count_overall = highest_count
                    highest_habit_id = i[0]
            return highest_habit_id, highest_count_overall
        else:
            return None

    def analyse_time(self, habit_id: int):
        all_events = self.database.select_get_habit_events(habit_id)
        if all_events:
            time_summary = 0
            for i in all_events:
                if i[2] == 1:
                    time_summary += i[3]
                else:
                    pass
            return time_summary
        else:
            return 0

    # Methods currently only used in unit testing

    def get_event_count(self, habit_id: int):
        habit_events = self.database.select_get_habit_events(habit_id)
        return len(habit_events)

    def manipulate_time(self, offset: int):
        """
        Currently only used in unit testing to go back in time\n
        :param offset: can be either a positive or negative number
        :return: Always True
        """
        self.date_today += timedelta(days=offset)
