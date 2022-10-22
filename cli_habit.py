"""Contains definitions of various cli parts and the general flow of the interaction with the cli."""
from typing import Union
from datetime import timedelta, datetime, date
from habit import Habit
from cli import Cli


# Definitions
def cli_definitions(cli: Cli, habit: Habit) -> None:
    """
    Contains the definitions for the cli interface, including menu-options and -functions.

    :param cli: a cli object
    :param habit: a habit object
    """
    cli.interactive_mode = True
    print("Interactive mode activated")
    # validate definitions
    cli.validate_functions.update({"name": ["max_length", 20],
                                   "description": ["max_length", 30],
                                   "periodicity": ["daily", "weekly"],
                                   "choice": ["y", "n"],
                                   "number": [0, 1440],
                                   "date": ["date", "date"],
                                   "alter": ["name", "description", "default time", "task"],
                                   "task": ["completion", "time"]})

    # question definitions
    cli.questions.update({"name": ["the habit name", "Any text is valid up to 20 letters"],
                          "description": ["the description of the habit", "Any text is valid up to 30 letters"],
                          "periodicity": ["the periodicity of the habit", "[daily] and [weekly]"],
                          "completed": ["if you completed this habit", "[y]es or [n]o"],
                          "time": ["a time value", "Any number up to 1440 is valid.\n"
                                                   "This is optional,if you want to skip this enter 0"],
                          "safety": ["if you are sure you want to do this action", "[y]es or [n]o"],
                          "database": ["if you want to load the sample database or use your own",
                                       "[y]es to use sample database or [n]o to use your own"],
                          "date": ["a valid date", "a valid date in the form YYYY-MM-DD (e.g. 2022-01-31)"],
                          "alter": ["what you want to alter", "[name], [description], [default time] or an existing "
                                                              "[task] record"],
                          "task": ["what you want to alter", "[completion] status or the [time] of the record"]})

    # main menu definitions
    cli.main_menu_name = "main"
    cli.main_menu_options.update({0: "Show menu",
                                  1: "Create a habit",
                                  2: "Update a habit",
                                  3: "Analyse habits",
                                  4: "Delete a habit",
                                  5: "Alter a habit",
                                  9: "Exit the application"})
    cli.main_menu_functions.update({
        0: lambda: cli.menu(),
        1: lambda: create_habit(cli, habit),
        2: lambda: update_habit(cli, habit),
        3: lambda: cli.menu(submenu_analyse_name, submenu_analyse_options, submenu_analyse_functions),
        4: lambda: delete_habit(cli, habit),
        5: lambda: alter_habit(cli, habit),
        9: lambda: [print("Exiting."), habit.database.close_connection(), exit()]})

    # analyse menu definitions
    submenu_analyse_name: str = "analyse"
    submenu_analyse_options: dict = {0: "Show menu",
                                     1: "Show all currently tracked habits",
                                     2: "Show all habits with the same periodicity",
                                     3: "Return the longest run streak of all defined habits",
                                     4: "Return the longest run streak for a given habit",
                                     5: "Return the time invested into a given habit",
                                     8: "Return to main menu"}
    submenu_analyse_functions: dict = {0: lambda: cli.menu(submenu_analyse_name, submenu_analyse_options,
                                                           submenu_analyse_functions),
                                       1: lambda: analyze_habits(cli, habit, "all"),
                                       2: lambda: analyze_habits(cli, habit, "all same periodicity"),
                                       3: lambda: analyze_habits(cli, habit, "longest streak of all"),
                                       4: lambda: analyze_habits(cli, habit, "longest streak"),
                                       5: lambda: analyze_habits(cli, habit, "time"),
                                       8: lambda: cli.menu()}

    # Dev mode is used to opt in developer options into the menu
    dev_mode = False
    if dev_mode:
        cli.main_menu_options.update({11: "manipulate time(+ or - number as days)", 12: "show db habits",
                                      13: "show db events"})
        cli.main_menu_functions.update({11: lambda: [habit.manipulate_time(offset=int(input())),
                                                     print(habit.date_today), cli.helper_wait_for_key()],
                                        12: lambda: [print(habit.database.read_habits()),
                                                     cli.helper_wait_for_key()],
                                        13: lambda: [print(habit.database.read_events()),
                                                     cli.helper_wait_for_key()]})
        habit.generate_new_dates = False
        cli.interactive_mode = False


# Helpers
def helper_type_conversions(argument: Union[str, bool, int]) -> Union[str, int]:
    """
    Convert types to a human-readable format or vice versa.

    :param argument: str daily or weekly, bool True or False, int 0, 1, 6 and 7
    :return: str daily returns int 1; str weekly returns int 7; bool True returns str successful;
     bool False returns str failed; int 0 returns str days, int 1 returns str daily; int 6 returns  str weeks;
     int 7 returns  str weekly
    """
    val: Union[str, int] = 0
    if type(argument) is str:
        if argument.casefold() == "daily":
            val = 1
        elif argument.casefold() == "weekly":
            val = 7
    if type(argument) is bool:
        if argument:
            val = "successful"
        else:
            val = "failed"
    if type(argument) is int:
        if argument == 0:
            val = "days"
        elif argument == 1:
            val = "daily"
        elif argument == 6:
            val = "weeks"
        elif argument == 7:
            val = "weekly"
    return val


def helper_format_and_output(result: list) -> None:
    """
    Format the habit details in a tabular form and print the table.

    :param result: list containing: id, name, description, periodicity, default_time_value, created_date
     and next_periodicity_due_date
    """
    print("{:20}  {:30}  {:8}  {:6}  {:10}  {:12}"
          .format("Name", "Description", "Periodicity", "Def. time", "Start date", "Due date"))
    print("{0:_^100}".format("_"))
    for i in result:
        name: str = str(i[1])
        description: str = str(i[2])
        periodicity: str = str(helper_type_conversions(i[3]))
        default_time_value: str = str(i[4])
        created_date: str = str(i[5])
        next_periodicity_due_date: str = str(i[6])
        formatted_output = ("{name:22}"
                            "{description:32}"
                            "{periodicity:13}"
                            "{default_time_value:11}"
                            "{created_date:12}"
                            "{next_periodicity_due_date:12}"
                            .format(name=name, description=description, periodicity=periodicity,
                                    default_time_value=default_time_value, created_date=created_date,
                                    next_periodicity_due_date=next_periodicity_due_date))
        print(formatted_output)


# General Flow
def create_habit(cli: Cli, habit: Habit) -> None:
    """
    Interactive mode flow for creating a habit.

    Steps:

    1: Ask for habit's name

    2: Ask for habit's description

    3: Ask for habit's periodicity

    4: Ask for habit's default time

    5: Output status of create, on success provide all details, on failure print error message

    :param cli: a cli object
    :param habit: a habit object
    """
    cli.helper_clear_terminal()
    print("Habit creating dialog")
    print("{0:_^100}".format("_"))
    habit.name = str(cli.validate("name", "name"))
    if not habit.is_existing(habit.name):
        habit.description = str(cli.validate("description", "description"))
        periodicity: str = str(cli.validate("periodicity", "periodicity"))
        habit.periodicity = int(helper_type_conversions(periodicity))
        habit.default_time = int(str(cli.validate("number", "time")))  # mypy is only happy with this construct...
        create_status = habit.create_habit(habit.name, habit.description, habit.periodicity)
        if create_status:
            cli.helper_clear_terminal()
            print("Successfully created the habit with details:")
            create_details = [(habit.unique_id,
                               habit.name, habit.description, habit.periodicity, habit.default_time,
                               habit.created_date, habit.next_periodicity_due_date)]
            helper_format_and_output(create_details)
        else:
            print(cli.message_error)
    else:
        print("A habit with the name \"{name}\" already exists!\nPlease choose another name!"
              .format(name=habit.name))
    cli.helper_wait_for_key()


def update_habit(cli: Cli, habit: Habit) -> None:
    """
    Interactive mode flow for updating a habit.

    Steps:

    1: Ask for habit's name

    2: Ask for habit's time

    3: Ask if habit's completed

    4: Output status of update, on success provide all details including possible fill dates, on failure print error
    message

    :param cli: a cli object
    :param habit: a habit object
    """
    cli.helper_clear_terminal()
    print("Habit update dialog")
    print("{0:_^100}".format("_"))
    habit.name = str(cli.validate("name", "name"))
    if habit.is_existing(habit.name):
        habit.time = int(str(cli.validate("number", "time")))  # mypy is only happy with this construct....
        habit.completed = bool(cli.validate("choice", "completed"))
        habit.set_id(habit.name)
        habit.set_next_periodicity_due_date(habit.unique_id)
        update_date: date = habit.next_periodicity_due_date
        create_status: tuple = habit.create_event(habit.name, habit.next_periodicity_due_date)
        completed: str = str(helper_type_conversions(habit.completed))
        if not habit.completed:
            habit.time = 0
        # Normal update
        if create_status[0] == "normal":
            cli.helper_clear_terminal()
            habit.next_periodicity_range_start = create_status[1][0]
            print("Successfully updated the habit \"{name}\".\n"
                  "Marked it as \"{completed}\" for due date "
                  "\"{update_date}\".\n"
                  "Added \"{time}\" minute/s.\n"
                  "The next routine for this habit needs to be checked until the end of the date "
                  "\"{next_periodicity_due_date}\"."
                  .format(name=habit.name, completed=completed,
                          update_date=update_date, time=habit.time,
                          next_periodicity_due_date=habit.next_periodicity_due_date))

        # Too early to update
        elif create_status[0] == "too early":
            cli.helper_clear_terminal()
            print("You cannot update the habit \"{name}\" at the moment!\nThe next time will be on the "
                  "\"{update_lower_range}\"".format(name=habit.name, update_lower_range=create_status[1][0]))

        # Update with fills
        elif create_status[0] == "with fill":
            cli.helper_clear_terminal()
            missed_dates = create_status[1]
            update_lower_range: date = create_status[1][0]
            update_date = update_lower_range + timedelta(days=habit.periodicity)
            if len(missed_dates) == 2:
                print("The habit was broken once since your last update!")
            else:
                print("The habit was broken {missed} times!".format(missed=len(missed_dates) - 1))
            for i in missed_dates:
                if i != 0:
                    missed_number = i
                    missed_lower_range: str = missed_dates[i]
                    missed_date: date = datetime.strptime(missed_lower_range,
                                                          habit.date_format).date() + timedelta(days=habit.periodicity)
                    print("Detected {number}. break of the habit \"{name}\". Marking as \"{completed}\" for due date "
                          "\"{update_lower_range}\""
                          .format(number=missed_number, name=habit.name, completed="failed",
                                  update_lower_range=missed_date))
            print("Successfully updated the habit \"{name}\".\n"
                  "Marked it as \"{completed}\" for due date "
                  "\"{update_date}\".\n"
                  "Added \"{time}\" minute/s.\n"
                  "The next routine for this habit needs to be checked until the end of the date "
                  "\"{next_periodicity_due_date}\"."
                  .format(name=habit.name, completed=completed,
                          update_date=update_date, time=habit.time,
                          next_periodicity_due_date=habit.next_periodicity_due_date))
        else:
            print(cli.message_error)
    else:
        print("The habit \"{name}\" does not exist!".format(name=habit.name))
    cli.helper_wait_for_key()


def analyze_habits(cli: Cli, habit: Habit, option: str) -> None:
    """
    Interactive mode flow for the decision chosen in the analyse submenu.

    Returns to the submenu after an output has been made.

    :param cli: a cli object
    :param habit: a habit object
    :param option: str "all", "all same periodicity", "longest streak of all" , "longest streak" or "time"
    """
    print("Habit analyse dialog")
    print("{0:_^100}".format("_"))
    # "Show all currently tracked habits"
    if option == "all":
        analyse_habits_all_active(cli, habit)
    # "Show all habits with the same periodicity"
    elif option == "all same periodicity":
        analyse_habits_same_periodicity(cli, habit)
    # "Return the longest run streak of all defined habits"
    elif option == "longest streak of all":
        analyse_all_habits_longest_streak(cli, habit)
    # "Return the longest run streak for a given habit"
    elif option == "longest streak":
        analyse_habit_longest_streak(cli, habit)
    # "Return the longest run streak for a given habit"
    elif option == "time":
        analyse_habit_time(cli, habit)
    cli.helper_wait_for_key()


def analyse_habits_all_active(cli: Cli, habit: Habit) -> None:
    """
    Interactive mode flow for analysing all active habits, prints out all in a tabular form.

    :param cli: a cli object
    :param habit: a habit object
    """
    result: list = habit.analyse_all_active()
    if result:
        cli.helper_clear_terminal()
        print("Showing all currently tracked habits:")
        if len(result) == 1:
            print("There is currently {number} habit:".format(number=len(result)))
        else:
            print("There are currently {number} habits:".format(number=len(result)))
        helper_format_and_output(result)
    else:
        print("There are currently no habits! Please create at-least one first!")


def analyse_habits_same_periodicity(cli: Cli, habit: Habit) -> None:
    """
    Interactive mode flow for analysing all active habits with the same periodicity, prints out all in a tabular form.

    :param cli: a cli object
    :param habit: a habit object
    """
    periodicity: str = str(cli.validate("periodicity", "periodicity"))
    habit.periodicity = int(helper_type_conversions(periodicity))
    same_periodicity_habits: list = habit.analyse_all_active_same_periodicity(habit.periodicity)
    if same_periodicity_habits:
        cli.helper_clear_terminal()
        print("Showing all currently tracked habits with the same periodicity of \"{periodicity}\":"
              .format(periodicity=periodicity))
        helper_format_and_output(same_periodicity_habits)
    else:
        print("There are currently no habits with a {periodicity} periodicity! Please create one first!"
              .format(periodicity=periodicity))


def analyse_all_habits_longest_streak(cli: Cli, habit: Habit) -> None:
    """
    Interactive mode flow for analysing the longest streak of all habits, prints the best habit and its streak.

    :param cli: a cli object
    :param habit: a habit object
    """
    highest_habit_id: int
    highest_count_overall: int
    if habit.analyse_longest_streak() != ():
        highest_habit_id, highest_count_overall = habit.analyse_longest_streak()
        if highest_habit_id == 0 or highest_count_overall in (1, 0):
            print("There is currently no streak ongoing at all!")
        else:
            habit.set_name(highest_habit_id)
            habit.set_id(habit.name)
            habit.set_periodicity(habit.unique_id)
            periodicity = helper_type_conversions(habit.periodicity - 1)
            cli.helper_clear_terminal()
            print("Showing the longest streak of all habits:")
            print(
                "The habit \"{name}\" is currently your best habit with a run streak of "
                "\"{highest_count_overall}\" {periodicity} in a row."
                .format(name=habit.name, highest_count_overall=highest_count_overall,
                        periodicity=periodicity))
    else:
        print("There are currently no habits! Please create at-least one first!")


def analyse_habit_longest_streak(cli: Cli, habit: Habit) -> None:
    """
    Interactive mode flow for analysing the longest streak of a given habit.

    Takes a name and will print the habit's streak.

    :param cli: a cli object
    :param habit: a habit object
    """
    name = str(cli.validate("name", "name"))
    if habit.is_existing(name):
        habit.set_id(name)
        highest_habit_id: int
        highest_count_overall: int
        highest_habit_id, highest_count_overall = habit.analyse_longest_streak(habit.unique_id)
        if highest_count_overall in (1, 0):
            print("The habit \"{name}\" does not have a streak currently!".format(name=name))
        else:
            habit.set_periodicity(highest_habit_id)
            periodicity: str = str(helper_type_conversions(habit.periodicity - 1))
            cli.helper_clear_terminal()
            print("Showing the longest streak for given habit:")
            print("The habit \"{name}\" best run streak is \"{highest_count}\" consecutive "
                  "{periodicity} in a row.".format(name=name, highest_count=highest_count_overall,
                                                   periodicity=periodicity))
    else:
        print("The habit \"{name}\" does not exist!".format(name=name))


def analyse_habit_time(cli: Cli, habit: Habit) -> None:
    """
    Interactive mode flow for analysing the time summary of a given habit.

    Takes a name and will print the habit's time summary in a formatted way as minutes, hours or days.

    :param cli: a cli object
    :param habit: a habit object
    """
    name = str(cli.validate("name", "name"))
    if habit.is_existing(name):
        habit.set_id(name)
        time_summary: float = habit.analyse_time(habit.unique_id)
        if time_summary == -1:
            print("There are currently no events for this habit! Please first update this habit at-least once!")
        elif time_summary == 0:
            print("There is currently no time tracked for the habit \"{name}\"!".format(name=name))
        else:
            time_unit: str = "minute/s"
            if 60 < time_summary < 1440:
                time_unit = "hour/s"
                time_summary = round(time_summary / 60, 2)
            elif time_summary > 1440:
                time_unit = "day/s"
                time_summary = round(time_summary / 1440, 2)
            cli.helper_clear_terminal()
            print("Showing the time summary for given habit:")
            print("You already spent on the habit \"{name}\" \"{time_summary}\" {time_unit}.".format(
                name=name, time_summary=time_summary, time_unit=time_unit))
    else:
        print("The habit \"{name}\" does not exist!".format(name=name))


def delete_habit(cli: Cli, habit: Habit) -> None:
    """
    Interactive mode flow for deleting a habit.

    Steps:

    1: Ask for habit's name

    2: Ask if user is sure

    3: Output status of delete, on success provide success message, on failure print error message

    :param cli: a cli object
    :param habit: a habit object
    """
    cli.helper_clear_terminal()
    print("Habit removal dialog")
    print("{0:_^100}".format("_"))
    habit.name = str(cli.validate("name", "name"))
    if habit.is_existing(habit.name):
        safety_ask: bool = bool(cli.validate("choice", "safety"))
        if safety_ask:
            habit.set_id(habit.name)
            delete_status = habit.delete(habit.unique_id)
            if delete_status:
                cli.helper_clear_terminal()
                print("Successfully removed the habit \"{name}\".".format(name=habit.name))
            else:
                print(cli.message_error)
        else:
            print("Removal was aborted.")
    else:
        print("The habit \"{name}\" does not exist!".format(name=habit.name))
    cli.helper_wait_for_key()


def alter_habit(cli: Cli, habit: Habit) -> None:
    """
    Interactive mode flow for altering a habit's details.

    Steps:

    1: Ask for habit's name

    2: Ask what the user wants to change, either the name, description, default time or a task record of a habit, if he
    decides to change a task he can either change the completion status or the time of the record

    3: Output status of alteration, on success provide success message, on failure print error message

    :param cli: a cli object
    :param habit: a habit object
    """
    cli.helper_clear_terminal()
    print("Habit alter dialog")
    print("{0:_^100}".format("_"))
    habit.name = str(cli.validate("name", "name"))
    habit.set_id(habit.name)
    if habit.is_existing(habit.name):
        alter_status: bool = False
        new_attribute: Union[str, int, bool] = ""
        alter_task_choice: str = ""
        record_exists: bool = False
        task_date: date = date.today()
        name_duplicate: bool = False
        alter_choice: str = str(cli.validate("alter", "alter"))
        if alter_choice.casefold() == "name":
            new_attribute = str(cli.validate("name", "name"))
            if habit.is_existing(new_attribute):
                name_duplicate = True
            else:
                alter_status = habit.alter_name(habit.unique_id, new_attribute)
        elif alter_choice.casefold() == "description":
            new_attribute = str(cli.validate("description", "description"))
            alter_status = habit.alter_description(habit.unique_id, new_attribute)
        elif alter_choice.casefold() == "default time":
            new_attribute = int(str(cli.validate("number", "time")))  # mypy is only happy with this construct...
            alter_status = habit.alter_default_time(habit.unique_id, new_attribute)
        elif alter_choice.casefold() == "task":
            record_exists, alter_task_choice, task_date, new_attribute, alter_status = alter_habit_task(cli, habit)
        if alter_status and alter_choice.casefold() != "task":
            cli.helper_clear_terminal()
            print("Successfully changed the \"{alter_choice}\" of habit \"{name}\" to \"{new_attribute}\"."
                  .format(alter_choice=alter_choice, name=habit.name, new_attribute=new_attribute))
        elif alter_status and alter_choice.casefold() == "task" and record_exists:
            cli.helper_clear_terminal()
            print("Successfully changed the \"{alter_task_choice}\" value of habit \"{name}\".\nThe value was changed "
                  "for the date \"{periodicity_date}\" to \"{new_attribute}\"."
                  .format(alter_task_choice=alter_task_choice, name=habit.name, periodicity_date=task_date,
                          new_attribute=new_attribute))
        elif alter_choice.casefold() == "task" and record_exists is False:
            print("There was no record found for this date!\nPlease keep in mind that the next periodicity date is a "
                  "due date and is therefor most times 1 periodicity ahead!")
        elif name_duplicate:
            print("There is already a habit with this name!\nPlease choose another name!")
        else:
            print(cli.message_error)
    else:
        print("The habit \"{name}\" does not exist!".format(name=habit.name))
    cli.helper_wait_for_key()


def alter_habit_task(cli: Cli, habit: Habit):
    """
    Interactive mode flow for altering a habit's task record.

    Steps:

    1: Ask for which date's a record should be searched for.

    2: If the record exists, ask the user what exactly he wants to change, either completion status or the time

    :param cli: a cli object
    :param habit: a habit object
    :return: record_exists bool if there is a record for given task, alter_task_choice str what the user wanted to
     change for given task, task_date date the user specified the task is, new_attribute str or int the new value the
     user has set, alter_status bool the status of the alteration
    """
    alter_task_choice: str = ""
    new_attribute: Union[str, int, bool] = 0
    alter_status: bool = False
    date_input = cli.validate("date", "date")
    task_date: date = datetime.strptime(str(date_input), habit.date_format).date()
    record_exists = habit.set_change_id(habit.unique_id, task_date)
    if record_exists:
        event_data: tuple = habit.get_event_data(habit.change_id)
        completed_status: bool = bool(event_data[2])
        time: int = event_data[3]
        completed: str = str(helper_type_conversions(completed_status))
        cli.helper_clear_terminal()
        print("There was a task found for the date {periodicity_date}.\nIt was marked as {completed} and a "
              "time of {time} minutes was recorded.".format(periodicity_date=task_date, completed=completed, time=time))
        alter_task_choice = str(cli.validate("task", "task"))
        if alter_task_choice.casefold() == "completion":
            new_attribute = bool(cli.validate("choice", "completed"))
            alter_status = habit.alter_event_completion(habit.change_id, new_attribute)
            new_attribute = helper_type_conversions(new_attribute)
        elif alter_task_choice.casefold() == "time":
            new_attribute = int(str(cli.validate("number", "time")))  # mypy is only happy with this construct...
            alter_status = habit.alter_event_time(habit.change_id, new_attribute)
    return record_exists, alter_task_choice, task_date, new_attribute, alter_status
