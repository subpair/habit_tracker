def cli_definitions(cli, habit) -> None:
    cli.interactive_mode = True
    print("Interactive mode activated")

    # validate definitions
    cli.validate_functions.update({"name": ["max_length", 20],
                                   "description": ["max_length", 30],
                                   "periodicity": ["daily", "weekly"],
                                   "choice": ["y", "n"],
                                   "number": [0, 1440]})

    # question definitions00000000
    cli.questions.update({"name": ["the habit name", "Any text is valid up to 20 letters"],
                          "description": ["the description of the habit", "Any text is valid up to 30 letters"],
                          "periodicity": ["the periodicity of the habit", "[daily] and [weekly]"],
                          "completed": ["if you completed this habit", "[y]es or [n]o"],
                          "time": ["a time value", "Any number up to 1440 is valid.\n"
                                                   "This is optional,if you want to skip this enter 0"],
                          "safety": ["if you are sure you want to do this action", "[y]es or [n]o"],
                          "database": ["if you want to load the sample database or use your own", "[y]es to use sample "
                                                                                                  "database or [n]o to use your own"]})

    # main menu definitions
    cli.main_menu_options.update({0: "Show menu",
                                  1: "Create a habit",
                                  2: "Update a habit",
                                  3: "Analyse habits",
                                  4: "Delete a habit",
                                  9: "Exit the application"})

    cli.main_menu_functions.update({
        0: lambda: cli.menu(),
        1: lambda: create_habit(cli, habit),
        2: lambda: update_habit(cli, habit),
        3: lambda: cli.menu(cli.submenu_analyse_name, cli.submenu_analyse_options, cli.submenu_analyse_functions),
        4: lambda: delete_habit(cli, habit),
        9: lambda: [print("Exiting."), habit.database.close_connection(), exit()]})

    # analyse menu definitions
    cli.submenu_analyse_name = "analyse"

    cli.submenu_analyse_options = {0: "Show menu",
                                   1: "Show all currently tracked habits",
                                   2: "Show all habits with the same periodicity",
                                   3: "Return the longest run streak of all defined habits",
                                   4: "Return the longest run streak for a given habit",
                                   5: "Return the time invested into a given habit",
                                   8: "Return to main menu"}

    cli.submenu_analyse_functions = {0: lambda: cli.menu(cli.submenu_analyse_name, cli.submenu_analyse_options,
                                                         cli.submenu_analyse_functions),
                                     1: lambda: analyze_habits(cli, habit, "all"),
                                     2: lambda: analyze_habits(cli, habit, "all same periodicity"),
                                     3: lambda: analyze_habits(cli, habit, "longest streak of all"),
                                     4: lambda: analyze_habits(cli, habit, "longest streak"),
                                     5: lambda: analyze_habits(cli, habit, "time"),
                                     8: lambda: cli.menu()}

    cli.message_error = "An unknown error occurred. Please copy the previous output and send it to developer :)"

    # DEV
    if cli.dev_mode:
        cli.main_menu_options.update({11: "manipulate time", 12: "show db habits", 13: "show db events"})
        cli.main_menu_functions.update({11: lambda: [habit.manipulate_time(offset=int(input())),
                                                     print(habit.date_today), cli.helper_wait_for_key()],
                                        12: lambda: [print(habit.database.read_habits()),
                                                     cli.helper_wait_for_key()],
                                        13: lambda: [print(habit.database.read_events()),
                                                     cli.helper_wait_for_key()]})


def helper_type_conversions(argument: str | bool | int) -> str | int:
    val: str | int = 0
    if type(argument) is str:
        if argument == "daily":
            val = 1
        elif argument == "weekly":
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
    Formatting the output of the analyse-functions in a tabular form\n
    :param result: the result of the function, consists of id, name, periodicity, default_time_value, created_date
     and next_periodicity_due_date
    :return: Always True
    """
    # print("{:25}  {:20}  {:1}  {:1}  {:12}  {:1}"
    print("{:20}  {:30}  {:8}  {:6}  {:10}  {:12}"
          .format("Name", "Description", "Periodicity", "Def. time", "Start date", "Due date"))
    print("{0:_^100}".format("_"))
    for i in result:
        name: str = i[1]
        description: str = i[2]
        periodicity: str = helper_type_conversions(i[3])
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


def create_habit(cli, habit) -> None:
    cli.helper_clear_terminal()
    print("Habit creating dialog")
    habit.name = cli.validate("name", "name")
    if not habit.is_existing(habit.name):
        habit.description = cli.validate("description", "description")
        periodicity: str = cli.validate("periodicity", "periodicity")
        habit.periodicity = helper_type_conversions(periodicity)
        habit.default_time = cli.validate("number", "time")
        create_status = habit.create_habit()
        if create_status:
            cli.helper_clear_terminal()
            habit.set_next_periodicity_due_date(habit.unique_id)
            print(
                "Successfully created the habit with details:")
            create_details = [(habit.unique_id,
                               habit.name, habit.description, habit.periodicity, habit.default_time,
                               habit.created_date, habit.next_periodicity_due_date)]
            helper_format_and_output(create_details)
            # "name: \"{name}\"\n"
            # "Description: \"{description}\"\n"
            # "Periodicity: \"{periodicity}\"\n"
            # "Next due until date: \"{next_periodicity_due_date}\"\n"
            # "Default time: \"{default_time}\" minutes"
            # .format(name=habit.name, description=habit.description, periodicity=periodicity,
            #         default_time=habit.default_time,
            #         next_periodicity_due_date=habit.next_periodicity_due_date))
        else:
            print(cli.message_error)
    else:
        print("A habit with the name \"{name}\" already exists!\nPlease choose another name!"
              .format(name=habit.name))
    cli.helper_wait_for_key()


def update_habit(cli, habit) -> None:
    cli.helper_clear_terminal()
    print("Habit update dialog")
    habit.name = cli.validate("name", "name")
    if habit.is_existing(habit.name):
        habit.set_id(habit.name)
        habit.set_periodicity(habit.unique_id)
        habit.set_next_periodicity_due_date(habit.unique_id)
        habit.set_default_time(habit.unique_id)
        habit.time = cli.validate("number", "time")
        habit.completed = cli.validate("choice", "completed")
        # This could be changed to make dynamic inserts instead of on next available date
        create_status = habit.create_event_logic(habit.next_periodicity_due_date)
        completed: str = helper_type_conversions(habit.completed)
        if create_status[0] == "normal":
            cli.helper_clear_terminal()
            habit.next_periodicity_range_start = create_status[1][0]
            print("Successfully updated the habit \"{name}\".\n"
                  "Marked it as \"{completed}\" for date "
                  "\"{next_periodicity_range_start}\".\n "
                  "Added \"{time}\" minute/s.\n"
                  "The next routine for this habit needs to be checked until the date \"{next_periodicity_due_date}\"."
                  .format(name=habit.name, completed=completed,
                          next_periodicity_range_start=habit.next_periodicity_range_start, time=habit.time,
                          next_periodicity_due_date=habit.next_periodicity_due_date))
        elif create_status[0] == "too early":
            cli.helper_clear_terminal()
            print("You cannot update the habit \"{name}\" at the moment! The next time will be on the "
                  "\"{update_lower_range}\"".format(name=habit.name, update_lower_range=create_status[1][0]))
        elif create_status[0] == "with fill":
            cli.helper_clear_terminal()
            missed_dates = create_status[1]
            habit.next_periodicity_range_start = create_status[1][0]
            if len(missed_dates) == 2:
                print("The habit was broken once since your last update!")
            else:
                print("The habit was broken {missed} times!".format(missed=len(missed_dates) - 1))
            for i in missed_dates:
                if i != 0:
                    missed_number = i
                    missed_date = missed_dates[i]
                    print("Detected {number}. break of the habit \"{name}\". Marking as \"{completed}\" for date "
                          "\"{update_lower_range}\""
                          .format(number=missed_number, name=habit.name, completed="failed",
                                  update_lower_range=missed_date))
            print("Successfully updated the habit \"{name}\" as \"{completed}\" for date "
                  "\"{next_periodicity_range_start}\" and added \"{time}\" minute/s.\nThe next routine for this habit needs"
                  " to be checked until the date \"{next_periodicity_due_date}\"."
                  .format(name=habit.name, completed=habit.completed,
                          next_periodicity_range_start=habit.next_periodicity_range_start, time=habit.time,
                          next_periodicity_due_date=habit.next_periodicity_due_date))
        else:
            print(cli.message_error)
    else:
        print("The habit \"{name}\" does not exist!".format(name=habit.name))
    cli.helper_wait_for_key()


def delete_habit(cli, habit) -> None:
    cli.helper_clear_terminal()
    print("Habit removal dialog")
    habit.name = cli.validate("name", "name")
    if habit.is_existing(habit.name):
        safety_ask: bool = cli.validate("choice", "safety")
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


def analyse_habits_all_active(cli, habit):
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
        print("There are currently no habits! Please create one first!")


def analyse_habits_same_periodicity(cli, habit):
    periodicity: str = cli.validate("periodicity", "periodicity")
    habit.periodicity = helper_type_conversions(periodicity)
    same_periodicity_habits: list = habit.analyse_all_active_same_periodicity(habit.periodicity)
    if same_periodicity_habits:
        cli.helper_clear_terminal()
        print("Showing all currently tracked habits with the same periodicity of \"{periodicity}\":"
              .format(periodicity=periodicity))
        helper_format_and_output(same_periodicity_habits)
    else:
        print("There are currently no habits with a {periodicity} periodicity! Please create one first!"
              .format(periodicity=periodicity))


def analyse_all_habits_longest_streak(cli, habit):
    highest_habit_id: int
    highest_count_overall: int
    highest_habit_id, highest_count_overall = habit.analyse_longest_streak()
    if highest_habit_id == 0 or highest_count_overall == 1 or highest_count_overall == 0:
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


def analyse_habit_longest_streak(cli, habit):
    name = cli.validate("name", "name")
    if habit.is_existing(name):
        habit.set_id(name)
        # TODO: annotation for tuple highest_habit_id, highest_count_overall?
        highest_habit_id, highest_count_overall = habit.analyse_longest_streak(habit.unique_id)
        if highest_habit_id == 0:
            print("The habit \"{name}\" was not updated yet!".format(name=name))
        elif highest_count_overall == 0 or highest_count_overall == 1:
            print("The habit \"{name}\" does not have a streak currently!".format(name=name))
        else:
            habit.set_periodicity(highest_habit_id)
            periodicity: str = helper_type_conversions(habit.periodicity - 1)
            cli.helper_clear_terminal()
            print("Showing the longest streak for given habit:")
            print("The habit \"{name}\" best run streak is \"{highest_count}\" consecutive "
                  "{periodicity} in a row.".format(name=name, highest_count=highest_count_overall,
                                                   periodicity=periodicity))
    else:
        print("The habit \"{name}\" does not exist!".format(name=name))


def analyse_habit_time(cli, habit):
    name = cli.validate("name", "name")
    if habit.is_existing(name):
        habit.set_id(name)
        time_summary: float = habit.analyse_time(habit.unique_id)
        if time_summary == 0:
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
            print("You already spend on the habit \"{name}\" \"{time_summary}\" {time_unit}.".format(
                name=name, time_summary=time_summary, time_unit=time_unit))
    else:
        print("The habit \"{name}\" does not exist!".format(name=name))


def analyze_habits(cli, habit, option: str) -> None:
    """
    The analyse-function will use the data from the database and give the user information about the existing data
    of the habits.\n
    :param option: can be "all", "all same periodicity", "longest streak of all", "longest streak" or "time"
    :return: always True
    """
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
    cli.menu(cli.submenu_analyse_name, cli.submenu_analyse_options, cli.submenu_analyse_functions)
