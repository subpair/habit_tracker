import sqlite3
from sqlite3 import connect, Error
from datetime import date


class Database:

    def __init__(self, file_name: str = None):
        """
        On initialization the database always needs a database file name, if none is given it will default to "main.db".
        Afterwards the connection is initiated. \n
        :param file_name: name of the database file
        """

        if file_name is None:
            file_name = "main.db"
        try:
            self.db_connection: sqlite3.Connection = connect(file_name)
        except Error as err:
            print(err)

    def close_connection(self) -> bool:
        """
        Close database connection \n
        :return: True on success, False on error
        """

        try:
            self.db_connection.close()
            return True
        except Error as err:
            print(err)
            return False

    # Initialization
    def initialize_database(self) -> bool:
        """
        Initializes the database with two tables: \n
        >habits
            This table stores the metadata of the habits which includes a name, description, periodicity, default_time,
            created_date, next_periodicity_due_date, finish_date and the finished status. \n
            Every entry in this table will get also a primary key assigned called unique_id.
        >habits_events
            This table stores the events for the habits which includes the habit_id as foreign key imported from the
            habits table, a completed status, a time value and a change_date. \n
        :return: True on successful run, False on database error
        """

        try:
            cur = self.db_connection.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS habits (
            unique_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT DEFAULT "" NOT NULL,
            periodicity INTEGER NOT NULL,
            default_time INTEGER DEFAULT 0 NOT NULL,
            created_date TIMESTAMP DATE NOT NULL,
            next_periodicity_due_date TIMESTAMP DATE,
            finish_date TIMESTAMP DEFAULT "31.12.2023" NOT NULL,
            finished BOOLEAN NOT NULL DEFAULT FALSE)""")

            cur.execute("""CREATE TABLE IF NOT EXISTS habits_events (
                change_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                time INTEGER DEFAULT 0 NOT NULL,
                change_date TIMESTAMP DATE NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits(unique_id))""")

            self.db_connection.commit()
            return True
        except Error as err:
            print(err)
            return False

    # Insert functions
    def insert_habit(self, name: str, description: str, periodicity: int, created_date: date,
                     next_periodicity_due_date: date, default_time: int) -> bool:
        """
        Inserts a new habit into the habits table \n
        :param name: the name of the habit
        :param description: the description of a habit
        :param periodicity: the periodicity of a habit as integer value
        :param created_date: the creation date of a habit
        :param next_periodicity_due_date: the last date a habit can be completed
        :param default_time: the default time value which is added on every successful event
        :return: True on successful run, False on database error
        """

        try:
            cur = self.db_connection.cursor()
            cur.execute(
                "INSERT or REPLACE INTO habits (name, description, periodicity, default_time, created_date, "
                "next_periodicity_due_date) VALUES (?, ?, ? , ?, ?, ?)",
                (name, description, periodicity, default_time, created_date, next_periodicity_due_date))
            self.db_connection.commit()
            return True
        except Error as err:
            print(err)
            return False

    def insert_event(self, habit_id: int, completed: bool, change_date: date, time: int) -> bool:
        """
        Inserts a new event into the habits_events table \n
        :param habit_id: the id of a habit to connect a change event with a specific habit
        :param completed: the status of the habit event
        :param change_date: the date on which the event occurred
        :param time: number of the time duration for an event
        :return: True on successful run, False on database error
        """

        if time is None:
            time = 0
        try:
            cur = self.db_connection.cursor()
            cur.execute(
                "INSERT INTO habits_events (habit_id, completed, time, change_date) VALUES (?, ?, ?, ?)",
                (habit_id, completed, time, change_date))
            self.db_connection.commit()
            return True
        except Error as err:
            print(err)
            return False

    # Select functions
    # habits table

    def select_get_habit_unique_id(self, name: str) -> tuple:
        """
        Get a single id via a name input \n
        :param name: the name of a habit
        :return: unique_id is returned if a record with the name exists, will be None if no record
        is found or a database error occurs
        """

        try:
            cur = self.db_connection.cursor()
            cur.execute("SELECT unique_id FROM habits WHERE name=?", (name,))
            return cur.fetchone()
        except Error as err:
            print(err)
            return ()

    def select_get_all_habits_unique_ids(self) -> list:
        """
        Get all existing habit ids \n
        :return: list of unique_id's is returned if a record with the name exists, will be an empty list if no record is
         found or a database error occurs
        """

        try:
            cur = self.db_connection.cursor()
            cur.execute("SELECT unique_id FROM habits")
            return cur.fetchall()
        except Error as err:
            print(err)
            return []

    def select_get_habit_name(self, unique_id: int) -> tuple:
        """
        Get the name via an id input \n
        :param unique_id: the id of a habit
        :return: name is returned if a record with the name exists, will be None if no record is found or a database
         error occurs
        """

        try:
            cur = self.db_connection.cursor()
            cur.execute("SELECT name FROM habits WHERE unique_id=?", (unique_id,))
            return cur.fetchone()
        except Error as err:
            print(err)
            return ()

    def select_periodicity(self, unique_id: int) -> tuple:
        """
        Get the periodicity via an input id \n
        :param unique_id: the id of a habit
        :return: periodicity as integer is returned, will be None if no record is found or a database error occurs
        """

        try:
            cur = self.db_connection.cursor()
            cur.execute("SELECT periodicity FROM habits WHERE unique_id=?", (unique_id,))
            return cur.fetchone()
        except Error as err:
            print(err)
            return ()

    def select_get_habit_default_time(self, unique_id: int) -> tuple:
        """
        Get the default_time via an input id \n
        :param unique_id: the id of a habit
        :return: the date default_time is returned, will be None if no record is found or a database error occurs
        """

        try:
            cur = self.db_connection.cursor()
            cur.execute("SELECT default_time FROM habits WHERE unique_id=?", (unique_id,))
            return cur.fetchone()
        except Error as err:
            print(err)
            return ()

    def select_next_periodicity_due_date(self, unique_id: int) -> tuple:
        """
        Get the next_periodicity_due_date via an input id \n
        :param unique_id: the id of a habit
        :return: the date next_periodicity_due_date is returned, will be None if no record is found or a database error
         occurs
        """

        try:
            cur = self.db_connection.cursor()
            cur.execute("SELECT next_periodicity_due_date FROM habits WHERE unique_id=?", (unique_id,))
            return cur.fetchone()
        except Error as err:
            print(err)
            return ()

    # habits_events table
    def select_get_habit_events(self, unique_id: int) -> list:
        """
        Gets all events for a specific habit via an input id \n
        :param unique_id: the id of a habit
        :return: all events for the input id are returned, will be an empty list if no record is found or a database
         error occurs
        """

        try:
            cur = self.db_connection.cursor()
            cur.execute("SELECT * FROM habits_events WHERE habit_id=?", (unique_id,))
            return cur.fetchall()
        except Error as err:
            print(err)
            return []

    # Update functions
    def update_next_periodicity_due_date(self, unique_id: int, next_periodicity_due_date: date) -> bool:
        """
        Updates the habits' table with a new next_periodicity_due_date \n
        :param unique_id: the id of a habit
        :param next_periodicity_due_date: the last date a habit can be completed
        :return: returns True on successful update, will be false if a database error occurs
        """

        try:
            cur = self.db_connection.cursor()
            cur.execute(
                "UPDATE habits SET next_periodicity_due_date=? WHERE unique_id=?",
                (next_periodicity_due_date, unique_id))
            self.db_connection.commit()
            return True
        except Error as err:
            print(err)
            return False

    # Delete functions
    def delete_habit_and_events(self, unique_id: int) -> bool:
        """
        Deletes a habit entry and all its events from the database \n
        :param unique_id: the id of a habit
        :return: returns True on successful deletion, will be false if a database error occurs
        """

        try:
            cur = self.db_connection.cursor()
            cur.execute(
                "DELETE FROM habits WHERE unique_id=?",
                (unique_id,))
            self.db_connection.commit()
            cur = self.db_connection.cursor()
            cur.execute(
                "DELETE FROM habits_events WHERE habit_id=?",
                (unique_id,))
            self.db_connection.commit()
            return True
        except Error as err:
            print(err)
            return False

    # Analyse functions
    def analyse_get_all(self) -> list:
        """
        Gets all habits that are active \n
        :return: returns all records from the habits' table which do not have the finished status, will be an empty list
         if no record is found or a database error occurs
        """

        try:
            cur = self.db_connection.cursor()
            cur.execute("SELECT * FROM habits WHERE finished=?", (False,))
            return cur.fetchall()
        except Error as err:
            print(err)
            return []

    def analyse_get_same_periodicity(self, periodicity: int) -> list:
        """
        Gets all habits with the same periodicity \n
        :param periodicity: an integer of allowed periodicity
        :return: returns all records from the habits' table which have the same periodicity entry, will be an empty list
         if no record is found or a database error occurs
        """

        try:
            cur = self.db_connection.cursor()
            cur.execute("SELECT * FROM habits WHERE periodicity=?", (periodicity,))
            return cur.fetchall()
        except Error as err:
            print(err)
            return []

    def select_get_all_habits(self) -> list:
        try:
            cur = self.db_connection.cursor()
            cur.execute("SELECT * FROM habits")
            return cur.fetchall()
        except Error as err:
            print(err)
            return []

    def select_structure(self) -> list:
        try:
            cur = self.db_connection.cursor()
            cur.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name")
            return cur.fetchall()
        except Error as err:
            print(err)
            return []
