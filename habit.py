from db import Database
from datetime import date, timedelta, datetime
from os import system


class Habit:
    def __init__(self, db_filename: str = "main.db"):
        """
        Initializing the necessary definition of a habit with name, description, periodicity and default_time_value\n
        Saving the current date and setting the date format for date to string conversion\n
        Connect to the database and initialize the tables if they do no exist yet\n
        Set interactive mode off by default for easier unittests/access to the class\n
        :param db_filename: the name of the database file as a string
        """

        self.name = [str]
        self.description = [str]
        self.periodicity = [str]
        self.default_time_value = [int]
        self.db_filename = db_filename
        self.database = Database(db_filename)
        self.database.initialize_database()
        self.date_format = "%Y-%m-%d"
        self.date_today = date.today()
        self.interactive_mode = False

    def create(self, name: str, description: str, periodicity: str, default_time: int):
        """
        Create the habit by preparing the parameters in the form of the database and run the database command\n
        :param name: the habit's name in text form
        :param description: the habit's description in text form
        :param periodicity: the habit's periodicity in text form
        :param default_time: the habit's default time in text form
        :return: False if the habit already exists, True on successful insert into the database
        """

        if self.database.select_get_habit_unique_id(name):
            self.helper_clear_terminal(self.interactive_mode)
            print("A habit with the name \"{name}\" already exists! Please choose another name!".format(name=name))
            self.helper_wait_for_key(self.interactive_mode)
            return False
        else:

            # Convert the input periodicity text to an integer and calculate the next_periodicity_due_date.
            periodicity = self.helper_periodicity(periodicity)
            next_periodicity_due_date = self.date_today + timedelta(days=periodicity)
            # Store the habit as record in the database
            self.database.insert_new_habit(name, description, periodicity, self.date_today,
                                           next_periodicity_due_date, default_time)

            self.helper_clear_terminal(self.interactive_mode)
            print("Successfully created habit \"{name}\" with the description \"{description}\" and a \"{periodicity}\""
                  " periodicity.\nThe first time it needs to be checked is until "
                  "the end of the \"{next_periodicity_due_date}\" and \"{default_time}\" minutes are added by default."
                  .format(name=name, description=description, periodicity=self.helper_periodicity(periodicity),
                          default_time=default_time, next_periodicity_due_date=next_periodicity_due_date))
            self.helper_wait_for_key(self.interactive_mode)
            return True

    def event(self, name: str, completed: bool, time: int):
        """
        Prepare the habit event for usage and call the update method, it is also checked if an event was missed and
        the record for this is inserted into the database.\n
        The events need to be checked if they are in the range of today to the next day or this or next week, as the
        user can create today a habit, complete it already today or go back tomorrow and tell the application it
        was completed for yesterday.\n
        :param name: the name of the habit
        :param completed: the status of the completion of a habit
        :param time: the time value of the habit event
        :return: True if an event was added to the database, False if no event was added to the database
        """

        # Check if the habit exists, if it's the case get its id, next periodicity due date, convert this to a date
        # (sqlite will return it as a string) , get the periodicity and calculate the lower range for which a habit can
        # be updated by subtracting the periodicity from the next periodicity due date
        if self.database.select_get_habit_unique_id(name):
            habit_id = self.database.select_get_habit_unique_id(name)[0]
            next_periodicity_due_date = self.database.select_next_periodicity_due_date(habit_id)[0]
            next_periodicity_due_date = datetime.strptime(next_periodicity_due_date, self.date_format).date()
            periodicity = self.database.select_periodicity(habit_id)[0]
            update_lower_range = next_periodicity_due_date - timedelta(days=periodicity)
            # Get the default time value from the database in case no time is passed
            if time == 0:
                time = self.database.select_get_habit_default_time(habit_id)[0]
            # If the current date is in the range of next_periodicity_due_date and this minus the periodicity the update
            # method is called
            if (self.date_today >= update_lower_range) and (self.date_today <= next_periodicity_due_date):
                self.update(habit_id, name, completed, update_lower_range, time, next_periodicity_due_date, periodicity)
                return True
            # If it is too early to update the habit, tell the user
            elif self.date_today < update_lower_range:
                self.helper_clear_terminal(self.interactive_mode)
                print("You cannot update the habit \"{name}\" at the moment! The next time will be on the "
                      "\"{update_lower_range}\"".format(name=name, update_lower_range=update_lower_range))
                self.helper_wait_for_key(self.interactive_mode)
                return True
            # If the user is already above the next periodicity due date calculate the number of times he missed the
            # habit already and fill failure events for these dates into the database and a normal update at the end
            elif self.date_today > next_periodicity_due_date:
                missed = int(((self.date_today - timedelta(days=periodicity)) - update_lower_range)
                             / timedelta(days=periodicity))
                for i in range(missed):
                    print("Detected {number}. break of the habit \"{name}\". Marking as \"{completed}\" for date "
                          "\"{update_lower_range}\""
                          .format(number=i + 1, name=name, completed="failure", update_lower_range=update_lower_range))
                    self.database.insert_new_event(habit_id, False, update_lower_range, 0)
                    next_periodicity_due_date += timedelta(days=periodicity)
                    self.database.update_next_periodicity_due_date(habit_id, next_periodicity_due_date)
                    update_lower_range = next_periodicity_due_date - timedelta(days=periodicity)
                if missed == 0:
                    print("The habit was broken once!")
                else:
                    print("The habit was broken {missed} times!".format(missed=missed + 1))
                self.helper_wait_for_key(self.interactive_mode)
                self.update(habit_id, name, completed, update_lower_range, time, next_periodicity_due_date, periodicity)
                return True
        else:
            self.helper_clear_terminal(self.interactive_mode)
            print("The habit \"{name}\" does not exist!".format(name=name))
            self.helper_wait_for_key(self.interactive_mode)
            return True

    def update(self, habit_id: int, name: str, completed: bool, update_lower_range: date, time: int,
               next_periodicity_due_date: date, periodicity: int):
        """
        Create a habit event by preparing the parameters in the form of the database and run the database command\n
        :param habit_id: the id of a habit
        :param name: the habit name
        :param completed: the status if the event was a success or failure
        :param update_lower_range: the date of the habit event
        :param time: the time that was invested into this habit event
        :param next_periodicity_due_date: the due date of the habit event
        :param periodicity: the periodicity of the habit
        :return: Always True
        """

        # Set time to 0 if the habit was a failure
        if not completed:
            time = 0
        # Insert the new habit event as record into the database
        self.database.insert_new_event(habit_id, completed, update_lower_range, time)
        # Calculate the next date on which the habit will be needed to complete and update the habit table with this
        next_periodicity_due_date += timedelta(days=periodicity)
        self.database.update_next_periodicity_due_date(habit_id, next_periodicity_due_date)

        completed = self.helper_completed(completed)
        self.helper_clear_terminal(self.interactive_mode)
        print("Successfully updated the habit \"{name}\" as \"{completed}\" for date \"{update_lower_range}\" and "
              "added \"{time}\" minutes.\nThe next routine for this habit needs to be checked until "
              "\"{next_periodicity_due_date}\"."
              .format(name=name, completed=completed, update_lower_range=update_lower_range, time=time,
                      next_periodicity_due_date=next_periodicity_due_date))
        self.helper_wait_for_key(self.interactive_mode)
        return True

    def remove(self, name: str, safety_ask: bool):
        """
        Remove a habit by preparing the parameters in the form of the database and run the database command\n
        :param name: the habit's name
        :param safety_ask: the answer of the safety question
        :return: True on completion, False if habit was not found or the action was aborted
        """

        # Only run the removal if the user accepted this, afterwards it is checked if there is an entry in the database
        # with the habit name, if this is the case the database command for removal is triggered
        if safety_ask:
            if self.database.select_get_habit_unique_id(name):
                habit_id = self.database.select_get_habit_unique_id(name)[0]
                self.database.delete_habit_and_events(habit_id)

                self.helper_clear_terminal(self.interactive_mode)
                print("Successfully removed the habit \"{name}\".".format(name=name))
                self.helper_wait_for_key(self.interactive_mode)
                return True
            else:
                print("The habit \"{name}\" does not exist!".format(name=name))
                self.helper_wait_for_key(self.interactive_mode)
                return False
        else:
            print("Removal was aborted.")
            return False

    def analyse(self, option: str, argument=None):
        """
        The analyse function will use the data from the database and give the user information about the existing data
        of the habits.\n
        :param option: can be "all", "all same periodicity", "longest streak of all", "longest streak" or "time"
        :param argument: can be None or for the parameters "all same periodicity" a periodicity as string or for
         "longest streak" a name as string
        :return: True if the parameter was successfully used, False if a step failed
        """
        # "Show all currently tracked habits"
        if option == "all":
            result = self.database.analyse_get_all()
            if result:
                self.helper_clear_terminal(self.interactive_mode)
                print("Showing all currently tracked habits:")
                if len(result) == 1:
                    print("There is currently {number} habit:".format(number=len(result)))
                else:
                    print("There are currently {number} habits:".format(number=len(result)))
                self.helper_format_and_output(result)
                self.helper_wait_for_key(self.interactive_mode)
                return True
            else:
                print("There are currently no habits! Please create one first!")
                self.helper_wait_for_key(self.interactive_mode)
                return False

        # "Show all habits with the same periodicity"
        elif option == "all same periodicity":
            periodicity = argument
            argument = self.helper_periodicity(argument)
            result = self.database.analyse_get_same_periodicity(argument)
            if result:
                self.helper_clear_terminal(self.interactive_mode)
                print("Showing all currently tracked habits with the same periodicity of \"{periodicity}\":"
                      .format(periodicity=periodicity))
                self.helper_format_and_output(result)
                self.helper_wait_for_key(self.interactive_mode)
                return True
            else:
                print("There are currently no habits! Please create one first!")
                self.helper_wait_for_key(self.interactive_mode)
                return False

        # "Return the longest run streak of all defined habits"
        elif option == "longest streak of all":
            # get all habits and their ids
            habit_ids = self.database.select_get_all_habits_unique_id()
            if habit_ids:
                # Count the number of times an event was successful for a habit by iterating over all events in all
                # existing habits.
                highest_count_overall = 0
                highest_habit_id = 0
                for i in habit_ids:
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
                # Check in general if it's a streak or just a single event.
                if highest_habit_id == 0 or 1 == highest_count_overall == 0:
                    print("There is currently no streak ongoing at all!")
                    self.helper_wait_for_key(self.interactive_mode)
                    return False
                else:
                    name = self.database.select_get_habit_name(highest_habit_id)[0]
                    periodicity = self.database.select_periodicity(highest_habit_id)[0]
                    periodicity = self.helper_periodicity_to_noun(periodicity)
                    self.helper_clear_terminal(self.interactive_mode)
                    print("Showing the longest streak of all habits:")
                    print(
                        "The habit \"{name}\" is currently your best habit with a run streak of "
                        "\"{highest_count_overall}\" {periodicity} in a row."
                        .format(name=name, highest_count_overall=highest_count_overall, periodicity=periodicity))
                    self.helper_wait_for_key(self.interactive_mode)
                    return True
            else:
                print("There are currently no habits! Please create one first!")
                self.helper_wait_for_key(self.interactive_mode)
                return False

        # "Return the longest run streak for a given habit"
        elif option == "longest streak":
            if self.database.select_get_habit_unique_id(argument):
                name = argument
                argument = self.database.select_get_habit_unique_id(argument)[0]
                all_events = self.database.select_get_habit_events(unique_id=argument)
                # This function is similar to the function from "longest streak of all" except that it only iterates
                # over the events of a single habit
                if all_events:
                    count = 0
                    highest_count = 0
                    for i in all_events:
                        if i[2] == 1:
                            count += 1
                        else:
                            count = 0
                        if count > highest_count:
                            highest_count = count
                    if count == 0 or count == 1:
                        print("The habit \"{name}\" does not have a streak currently!".format(name=name))
                        self.helper_wait_for_key(self.interactive_mode)
                        return False
                    else:
                        self.helper_clear_terminal(self.interactive_mode)
                        periodicity = self.database.select_periodicity(argument)[0]
                        periodicity = self.helper_periodicity_to_noun(periodicity)
                        print("Showing the longest streak for given habit:")
                        print(
                            "The habit \"{name}\" best run streak is \"{highest_count}\" consecutive "
                            "{periodicity} in a row.".format(name=name, highest_count=highest_count,
                                                             periodicity=periodicity))
                        self.helper_wait_for_key(self.interactive_mode)
                        return True
                else:
                    print("The habit \"{name}\" was not updated yet!".format(name=name))
                    self.helper_wait_for_key(self.interactive_mode)
                    return False
            else:
                print("The habit \"{name}\" does not exist!".format(name=argument))
                self.helper_wait_for_key(self.interactive_mode)
                return False

        # "Return the longest run streak for a given habit"
        elif option == "time":
            if self.database.select_get_habit_unique_id(argument):
                name = argument
                argument = self.database.select_get_habit_unique_id(argument)[0]
                all_events = self.database.select_get_habit_events(unique_id=argument)
                if all_events:
                    time_summary = 0
                    for i in all_events:
                        if i[2] == 1:
                            time_summary += i[3]
                        else:
                            pass
                    self.helper_clear_terminal(self.interactive_mode)
                    if time_summary == 0:
                        print("There is currently no time tracked for the habit \"{name}\"!".format(name=name))
                        self.helper_wait_for_key(self.interactive_mode)
                        return False
                    else:
                        time_unit = ["minutes", "hours", "days"]
                        if 60 < time_summary < 1440:
                            time_unit = time_unit[1]
                            time_summary = round(time_summary / 60, 2)
                        elif time_summary > 1440:
                            time_unit = time_unit[2]
                            time_summary = round(time_summary / 1440, 2)
                        else:
                            time_unit = time_unit[0]
                        print("Showing the time summary for given habit:")
                        print("You already spend on the habit \"{name}\" \"{time_summary}\" {time_unit}.".format(
                            name=name,
                            time_summary=time_summary, time_unit=time_unit))
                        self.helper_wait_for_key(self.interactive_mode)
                        return True
                else:
                    print("There is currently no time tracked for the habit \"{name}\"!".format(name=name))
                    self.helper_wait_for_key(self.interactive_mode)
                    return False
            else:
                print("The habit \"{name}\" does not exist!".format(name=argument))
                self.helper_wait_for_key(self.interactive_mode)
                return False

    def helper_format_and_output(self, result: list):
        """
        Formatting the output of the analyse functions in a tabular form\n
        :param result: the result of the function, consists of id, name, periodicity, default_time_value, created_date
         and next_periodicity_due_date
        :return: Always True
        """

        print("{:20}  {:35}  {:10}  {:10}  {:15}  {:15}"
              .format("Name", "Description", "Periodicity", "Default time", "Creation date", "Next due date"))
        print("{0:_^120}".format("_"))
        for i in result:
            name = i[1]
            description = i[2]
            periodicity = i[3]
            periodicity = self.helper_periodicity(periodicity)
            default_time_value = i[4]
            created_date = i[5]
            next_periodicity_due_date = i[6]
            formatted_output = ("{name:20}\t"
                                "{description:35}\t"
                                "{periodicity:10}\t"
                                "{default_time_value:5}\t"
                                "{created_date:15}\t"
                                "{next_periodicity_due_date:15}\t".format(name=name, description=description,
                                                                          periodicity=periodicity,
                                                                          default_time_value=default_time_value,
                                                                          created_date=created_date,
                                                                          next_periodicity_due_date=next_periodicity_due_date))
            print(formatted_output)
        return True

    @staticmethod
    def helper_periodicity(periodicity: str or int):
        """
        Convert the periodicity text to number or number to text\n
        :param periodicity: can be either the text or the number value of periodicity
        :return: if string is given 1 or 7, if integer is given "daily" or "weekly"
        """

        if type(periodicity) is str:
            if periodicity == "daily".casefold():
                return 1
            elif periodicity == "weekly".casefold():
                return 7
        elif type(periodicity) is int:
            if periodicity == 1:
                return "daily"
            elif periodicity == 7:
                return "weekly"

    @staticmethod
    def helper_periodicity_to_noun(periodicity: int):
        """
        Convert the periodicity number to a text in form of a noun\n
        :param periodicity: the number value of periodicity
        :return: if given 1 "days", if given 7 "weeks"
        """

        if periodicity == 1:
            return "days"
        elif periodicity == 7:
            return "weeks"

    @staticmethod
    def helper_completed(completed: int):
        """
        Convert the completed integer to a text form\n
        :param completed: the number value of completed
        :return: if given 1 "success", if given 0 "failure"
        """

        if completed == 1:
            return "success"
        elif completed == 0:
            return "failure"

    @staticmethod
    def helper_clear_terminal(interactive_mode: bool = True):
        """
        Clears the terminal for better and clearer visibility\n
        :param interactive_mode: option to set the clearing on or off
        :return: True if input parameter is True, False otherwise
        """

        if interactive_mode:
            system('cls||clear')
            return True
        else:
            return False

    @staticmethod
    def helper_wait_for_key(interactive_mode: bool = True):
        """
        Simple input function with text to give the user the chance to read his last actions\n
        :param interactive_mode: option to set the clearing on or off
        :return: True if input parameter is True, False otherwise
        """

        if interactive_mode:
            input("...press enter to continue...\n>")
            return True
        else:
            return False

    # dev method for unit testing
    def manipulate_time(self, offset: int):
        """
        Currently only used in unit testing to go back in time\n
        :param offset: can be either a positive or negative number
        :return: Always True
        """
        self.date_today += timedelta(days=offset)
        print("the new date is {date}".format(date=self.date_today))
        return True
