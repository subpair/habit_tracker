"""Contains all database commands."""
import sqlite3
from sqlite3 import connect, Error
from datetime import date


class Database:
    """Database class for interacting with the database."""

    def __init__(self, file_name: str = None):
        """
        Initialize the database.

        On initialization the database always needs a database file name, if none is given it will default to "main.db".
        Afterwards the connection is initiated.

        :param file_name: name of the database file
        """
        if file_name is None:
            self.file_name = "main.db"
        self.file_name = str(file_name)
        try:
            self.db_connection: sqlite3.Connection = connect(self.file_name)
        except Error as err:
            print(err)

    # Connection
    def open_connection(self) -> bool:
        """
        Open the database connection.

        :return: True on success, False on error
        """
        try:
            self.db_connection = connect(self.file_name)
            return True
        except Error as err:
            print(err)
            return False

    def close_connection(self) -> bool:
        """
        Close the database connection.

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
        Initialize the database with two tables.

        >habits
            This table stores the metadata of the habits which includes a name, description, periodicity, default_time,
            created_date, next_periodicity_due_date, finish_date and the finished status.

            Every entry in this table will get also a primary key assigned called unique_id.

        >habits_events
            This table stores the events for the habits which includes the habit_id as foreign key imported from the
            habits table, a completed status, a time value and a change_date.

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

    # Creation
    def create_new_habit(self, name: str, description: str, periodicity: int, created_date: date,
                         next_periodicity_due_date: date, default_time: int) -> bool:
        """
        Insert a new habit into the habits table.

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

    def create_new_event(self, habit_id: int, completed: bool, change_date: date, time: int) -> bool:
        """
        Insert a new event into the habits_events table.

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

    # Reading
    #   habits table
    def read_habit_unique_id(self, name: str) -> tuple:
        """
        Get a single unique id via a name input from the habits table.

        :param name: the name of a habit
        :return: tuple unique_id is returned if a record with the name exists, will be an empty tuple if no record is
         found or a database error occurs
        """
        try:
            cur = self.db_connection.cursor()
            cur.execute("SELECT unique_id FROM habits WHERE name=?", (name,))
            return cur.fetchone()
        except Error as err:
            print(err)
            return ()

    def read_habits_unique_ids(self) -> list:
        """
        Get all existing habit unique ids from the habits table.

        :return: list of unique_id's is returned , will be an empty list if no record is found or a database error
         occurs
        """
        try:
            cur = self.db_connection.cursor()
            cur.execute("SELECT unique_id FROM habits")
            return cur.fetchall()
        except Error as err:
            print(err)
            return []

    def read_habit_name(self, unique_id: int) -> tuple:
        """
        Get the name via an id input from the habits table.

        :param unique_id: the id of a habit
        :return: tuple with str name , will be an empty tuple if no record is found or a database error occurs
        """
        try:
            cur = self.db_connection.cursor()
            cur.execute("SELECT name FROM habits WHERE unique_id=?", (unique_id,))
            return cur.fetchone()
        except Error as err:
            print(err)
            return ()

    def read_habit_periodicity(self, unique_id: int) -> tuple:
        """
        Get the periodicity via an input id from the habits table.

        :param unique_id: the id of a habit
        :return: tuple with int periodicity, will be an empty tuple  if no record is found or a database error occurs
        """
        try:
            cur = self.db_connection.cursor()
            cur.execute("SELECT periodicity FROM habits WHERE unique_id=?", (unique_id,))
            return cur.fetchone()
        except Error as err:
            print(err)
            return ()

    def read_habit_default_time(self, unique_id: int) -> tuple:
        """
        Get the default_time via an input id from the habits table.

        :param unique_id: the id of a habit
        :return: tuple with date default_time, will be an empty tuple  if no record is found or a database error occurs
        """
        try:
            cur = self.db_connection.cursor()
            cur.execute("SELECT default_time FROM habits WHERE unique_id=?", (unique_id,))
            return cur.fetchone()
        except Error as err:
            print(err)
            return ()

    def read_next_periodicity_due_date(self, unique_id: int) -> tuple:
        """
        Get the next_periodicity_due_date via an input id from the habits table.

        :param unique_id: the id of a habit
        :return: tuple with date next_periodicity_due_date, will be an empty tuple  if no record is found or a database
         error occurs
        """
        try:
            cur = self.db_connection.cursor()
            cur.execute("SELECT next_periodicity_due_date FROM habits WHERE unique_id=?", (unique_id,))
            return cur.fetchone()
        except Error as err:
            print(err)
            return ()

    #   habits_events table
    def read_habit_events(self, unique_id: int) -> list:
        """
        Get all events for a specific habit via an input id from the habits_events table.

        :param unique_id: the id of a habit
        :return: list with all events for the input id is returned, will be an empty list if no record is found or a
         database error occurs
        """
        try:
            cur = self.db_connection.cursor()
            cur.execute("SELECT * FROM habits_events WHERE habit_id=?", (unique_id,))
            return cur.fetchall()
        except Error as err:
            print(err)
            return []

    # Updating
    def update_next_periodicity_due_date(self, unique_id: int, next_periodicity_due_date: date) -> bool:
        """
        Update an entry in the habits table with a new next_periodicity_due_date.

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

    # Deletion
    def delete_habit_and_events(self, unique_id: int) -> bool:
        """
        Delete a habit entry from the habits table and all its events in the habits_events table from the database.

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

    # Analyse
    def read_habits_by_not_finished(self) -> list:
        """
        Get all habits that are active from the habits table.

        :return: list of all records from the habits table which do not have the finished status, will be an empty list
         if no record is found or a database error occurs
        """
        try:
            cur = self.db_connection.cursor()
            cur.execute("SELECT * FROM habits WHERE finished=?", (False,))
            return cur.fetchall()
        except Error as err:
            print(err)
            return []

    def read_habits_by_periodicity(self, periodicity: int) -> list:
        """
        Get all habits with the same periodicity from the habits table.

        :param periodicity: integer of allowed periodicity
        :return: returns all records from the habits table which have the same periodicity entry, will be an empty list
         if no record is found or a database error occurs
        """
        try:
            cur = self.db_connection.cursor()
            cur.execute("SELECT * FROM habits WHERE periodicity=?", (periodicity,))
            return cur.fetchall()
        except Error as err:
            print(err)
            return []

    # Development and unittest
    def read_habits(self) -> list:
        """
        Get all habits from the habits table.

        :return: list of all records from the habits table, will be an empty list if no record is found or a database
         error occurs
        """
        try:
            cur = self.db_connection.cursor()
            cur.execute("SELECT * FROM habits")
            return cur.fetchall()
        except Error as err:
            print(err)
            return []

    def read_events(self) -> list:
        """
        Get all events from the habits_events table.

        :return: list of all records from the habits_events table, will be an empty list if no record is found or a
         database error occurs
        """
        try:
            cur = self.db_connection.cursor()
            cur.execute("SELECT * FROM habits_events")
            return cur.fetchall()
        except Error as err:
            print(err)
            return []

    def read_database_structure(self) -> list:
        """
        Get the current existing tables in the database.

        :return: list of all tables from the sqlite_schema table, will be an empty list if no record is found or a
         database error occurs
        """
        try:
            cur = self.db_connection.cursor()
            cur.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name")
            return cur.fetchall()
        except Error as err:
            print(err)
            return []
