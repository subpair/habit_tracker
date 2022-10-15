"""Contains the habit tracker logic."""
from datetime import date, timedelta, datetime
from db import Database


class Habit:
    """Habit class for the general habit tracker logic."""

    def __init__(self, name: str = None, description: str = None, periodicity: int = None, default_time: int = None,
                 db_filename: str = None, user_mode: bool = None) -> None:
        """
        Initialize the necessary definition of a habit with name, description, periodicity and default_time_value.

        Saving the current date and setting the date format for date to string conversion

        Connect to the database using db_filename.

        :param name: str name of a habit (default "")
        :param description: str description of a habit (default "")
        :param periodicity: int periodicity of a habit (currently only 1 and 7 is supported) (default 0)
        :param default_time: int default time of a habit (default 0)
        :param db_filename: str name of the database file (default main.db)
        :param user_mode: bool, if True it will generate a new date on every create/update event
        """
        if name is None:
            self.name: str = ""
        else:
            self.name = name

        if description is None:
            self.description: str = ""
        else:
            self.description = description

        if periodicity is None:
            self.periodicity: int = 0
        else:
            self.periodicity = periodicity

        if default_time is None:
            self.default_time: int = 0
        else:
            self.default_time = default_time

        if db_filename is None:
            self.db_filename: str = "main.db"
        else:
            self.db_filename = db_filename

        if user_mode is None:
            self.user_mode: bool = True
        else:
            self.user_mode = user_mode

        self.completed: bool = False

        self.database = Database(self.db_filename)
        self.time: int = 0
        self.unique_id: int = 0

        self.date_format: str = "%Y-%m-%d"
        self.date_today: date = date.today()
        self.created_date: date = date.today()
        self.next_periodicity_due_date: date = date.today()
        self.next_periodicity_range_start: date = date.today()
        self.initialize_database()

    def initialize_database(self) -> None:
        """Call the database initialization method which creates two tables."""
        self.database.initialize_database()

    def is_existing(self, habit_name: str) -> bool:
        """
        Check if there is a database entry for given name.

        :param habit_name: str name of a habit
        :return: bool True if there is a record, False if there is none
        """
        return self.database.read_habit_unique_id(habit_name) is not None

    def set_id(self, habit_name: str) -> bool:
        """
        Set the habit unique id value for given name.

        :param habit_name: str name of a habit
        :return: bool True if there is an id found in the database, False if there is none
        """
        unique_id: tuple = self.database.read_habit_unique_id(habit_name)
        if unique_id is not None:
            self.unique_id = unique_id[0]
            return True
        return False

    def set_periodicity(self, habit_id: int) -> bool:
        """
        Set the habit periodicity value for given id.

        :param habit_id: int id of a habit
        :return: bool True if there is a periodicity found in the database, False if there is none
        """
        periodicity: tuple = self.database.read_habit_periodicity(habit_id)
        if periodicity is not None:
            self.periodicity = periodicity[0]
            return True
        return False

    def set_next_periodicity_due_date(self, habit_id: int) -> bool:
        """
        Set the habit next periodicity due date value for given id.

        :param habit_id: int id of a habit
        :return: bool True if there is a habit next periodicity due date found in the database, False if there is none
        """
        next_periodicity_due_date: tuple = self.database.read_next_periodicity_due_date(habit_id)
        if next_periodicity_due_date is not None:
            self.next_periodicity_due_date = datetime.strptime(next_periodicity_due_date[0], self.date_format).date()
            return True
        return False

    def set_default_time(self, habit_id: int) -> bool:
        """
        Set the habit default time value for given id.

        :param habit_id: int id of a habit
        :return: bool True if there is a default time found in the database, False if there is none
        """
        default_time: tuple = self.database.read_habit_default_time(habit_id)
        if default_time is not None:
            self.default_time = default_time[0]
            return True
        return False

    def set_name(self, habit_id: int) -> bool:
        """
        Set the habit name value for given id.

        :param habit_id: int id of a habit
        :return: bool True if there is a name found in the database, False if there is none
        """
        name: tuple = self.database.read_habit_name(habit_id)
        if name is not None:
            self.name = name[0]
            return True
        return False

    def create_habit(self, created_date: date = None, next_periodicity_due_date: date = None) -> bool:
        """
        Insert a new habit into the habits table.

        :param created_date: date of the change
        :param next_periodicity_due_date: date of next periodicity due date
        :return: bool True if the creation was successful, False if not or a database error occurred
        """
        if created_date is None:
            if self.user_mode:
                created_date = date.today()
            else:
                created_date = self.date_today
            self.created_date = created_date
        if next_periodicity_due_date is None:
            next_periodicity_due_date = self.created_date + timedelta(days=self.periodicity)
        self.next_periodicity_due_date = next_periodicity_due_date
        create_status = self.database.create_new_habit(self.name, self.description, self.periodicity,
                                                       self.created_date, self.next_periodicity_due_date,
                                                       self.default_time)
        return create_status

    def create_event_update(self, completed: bool, next_periodicity_due_date: date, change_date: date = None) \
            -> bool:
        """
        Insert a new event into the habits_events table.

        If the user mode is active a new date will be created, else it will use the date provided. When the time value
        is 0, default time will be used.

        If completed is False the time value will be set to 0, else it will use the time provided.

        :param completed: bool True if the habit was a success, False if not
        :param next_periodicity_due_date: date of next periodicity due date
        :param change_date: date of the change
        :return: bool True if the creation was successful, False if not or a database error occurred
        """
        if change_date is None:
            if self.user_mode:
                change_date = date.today()
            else:
                change_date = self.date_today
        if self.time == 0:
            self.time = self.default_time
        if not completed:
            time = 0
        else:
            time = self.time
        create_status = self.database.create_new_event(self.unique_id, completed, change_date, time)
        if create_status is not None:
            self.next_periodicity_due_date = next_periodicity_due_date + timedelta(days=self.periodicity)
            self.database.update_next_periodicity_due_date(self.unique_id, self.next_periodicity_due_date)
        return create_status

    def create_event(self, name: str, next_periodicity_due_date: date, change_date: date = None) \
            -> tuple[str, dict]:
        """
        Event logic, to decide if it is a simple update, too early to update or an update with additional fills.

        :param name: str habit name
        :param next_periodicity_due_date: date next_periodicity_due_date
        :param change_date: date of change
        :return: str status and dict missed_dates, status can be "normal","too early" or "with fill".
         missed_dates always provides on the first (0) key the current periodicity range start as date, on a fill the
         fills are starting at the second (1) key with their dates as values.
        """
        if self.is_existing(name):
            self.set_id(name)
            self.set_periodicity(self.unique_id)
            self.set_next_periodicity_due_date(self.unique_id)
            self.set_default_time(self.unique_id)
        status: str = ""
        missed_dates: dict = {}
        if change_date is None:
            if self.user_mode:
                change_date = date.today()
            else:
                change_date = self.date_today
        update_lower_range: date = next_periodicity_due_date - timedelta(days=self.periodicity)
        if next_periodicity_due_date >= change_date >= update_lower_range:
            self.create_event_update(self.completed, self.next_periodicity_due_date, change_date=change_date)
            status = "normal"
            missed_dates[0] = change_date
        elif change_date < update_lower_range:
            status = "too early"
            missed_dates[0] = update_lower_range
        elif change_date > next_periodicity_due_date:
            status = "with fill"
            update_lower_range, missed_dates = self.create_event_fill(update_lower_range)
            self.create_event_update(self.completed, self.next_periodicity_due_date, update_lower_range)
            missed_dates[0] = update_lower_range
        return status, missed_dates

    def create_event_fill(self, update_lower_range: date) -> tuple[date, dict]:
        """
        Fill events if there are missed events.

        :param update_lower_range: date of lower range of next periodicity due date
        :return: dict of number of miss and the date when this miss occurred. This dict uses a human-readable format and
         starts at 1
        """
        missed: int = int(((self.date_today - timedelta(days=self.periodicity)) - update_lower_range) / timedelta(
            days=self.periodicity))
        missed_dates: dict = {}
        for i in range(missed):
            missed_dates[i + 1] = str(update_lower_range)
            self.create_event_update(False, self.next_periodicity_due_date, update_lower_range)
            self.database.update_next_periodicity_due_date(self.unique_id, self.next_periodicity_due_date)
            update_lower_range = self.next_periodicity_due_date - timedelta(days=self.periodicity)
        return update_lower_range, missed_dates

    def analyse_all_active(self) -> list:
        """
        Read all habit records from the database that do not have the status finished.

        :return: list of all habits in format [id, name, description, periodicity, default_time, created_date,
         next_periodicity_due_date]
        """
        result: list = self.database.read_habits_by_not_finished()
        return result

    def analyse_all_active_same_periodicity(self, periodicity: int) -> list:
        """
        Read all habit records from the database that do not have the status finished and share the same periodicity.

        :param periodicity: int periodicity (currently 1 or 7)
        :return: list of all habits in format [id, name, description, periodicity, default_time, created_date,
         next_periodicity_due_date]
        """
        result: list = self.database.read_habits_by_periodicity(periodicity)
        return result

    def analyse_longest_streak(self, habit_id: int = None) -> tuple:
        """
        Read all habit events from the habits_events table and calculates the longest streak.

        If a habit id is provided it will check only the events of this one, if none is provided all habits and their
        events will be considered.

        :param habit_id: int the id of a habit
        :return: tuple of (highest_habit_id, highest_count_overall) or empty tuple if no streak was found
        """
        if habit_id is None:
            habit_unique_ids: list = self.database.read_habits_unique_ids()
        else:
            habit_unique_ids = [(habit_id,)]
        if habit_unique_ids:
            # Count the number of times an event was successful for a habit by iterating over all events in all
            # existing habits.
            highest_count_overall: int = 0
            highest_habit_id: int = 0
            for i in habit_unique_ids:
                all_events = self.database.read_habit_events(unique_id=i[0])
                count: int = 0
                highest_count: int = 0
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
        return ()

    def analyse_time(self, habit_id: int) -> int:
        """
        Read all habit events for the given habit id from the habits_events table and calculates the time summary.

        :param habit_id: int the id of a habit
        :return: int time_summary  or -1 if no events were found
        """
        all_events: list = self.database.read_habit_events(habit_id)
        if all_events:
            time_summary: int = 0
            for i in all_events:
                if i[2] == 1:
                    time_summary += i[3]
                else:
                    pass
            return time_summary
        return -1

    def delete(self, habit_id: int) -> bool:
        """
        Delete a habit and all its events from the database.

        :param habit_id: int id of a habit
        :return: bool True if the removal was successful, False if not or a database error occurred
        """
        delete = self.database.delete_habit_and_events(habit_id)
        return delete

    # Methods currently only used in developer options or unit testing
    def get_event_count(self, habit_id: int) -> int:
        """
        Read all events from the database and output the count as a number of these.

        :param habit_id: int id of a habit
        :return: int the length of all events
        """
        habit_events: list = self.database.read_habit_events(habit_id)
        return len(habit_events)

    def manipulate_time(self, offset: int) -> None:
        """
        Offset the current date_today by an int to go back in time or into the future.

        :param offset: int negative or positive number as days
        """
        self.date_today += timedelta(days=offset)
