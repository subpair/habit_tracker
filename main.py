from cli import Cli
from habit import Habit
from sample_data import SampleData

if __name__ == "__main__":
    cli = Cli()
    habit = Habit()
    try:
        habit.interactive_mode = True
        print("Interactive mode activated")

        # Menu Builder
        # The Menu consist of:
        # - %name%menu_name string ""
        # contains the name of the menu
        #
        # - %name%menu_options dictionary {integer, string}
        # holds the number with which the option can be chosen and a description of this option
        #
        # - %name%menu_functions dictionary {integer, lambda: function or list of functions in order}
        # connects the number of the menu_options with a functionality, which is called through a lambda function
        #
        # %name% can be anything, but any menu needs these 3 to have something displayed
        #
        #
        # Example:
        #         mainmenu_options[5] = "Print Hello World"
        #         mainmenu_functions[5] = lambda: [print("Hello "), print("World")]
        #         This will add a new function to the menu, which will print 2 strings when the number 5 is chosen

        # main menu definitions
        mainmenu_name = "Main"

        mainmenu_options = {1: "Create a habit",
                            2: "Update a habit",
                            3: "Analyse habits",
                            4: "Delete a habit",
                            9: "Exit the application"}

        mainmenu_functions = {
            1: lambda: [habit.helper_clear_terminal(), print("Habit Creating Dialog"),
                        habit.create(name=cli.validate("name", "name"),
                                     description=cli.validate("description", "description"),
                                     periodicity=cli.validate("periodicity", "periodicity"),
                                     default_time=cli.validate("number", "time"))],
            2: lambda: [habit.helper_clear_terminal(), print("Habit Update Dialog"),
                        habit.event(name=cli.validate("name", "name"),
                                    time=cli.validate("number", "time"),
                                    completed=cli.validate("choice", "completed"))],
            3: lambda: [habit.helper_clear_terminal(),
                        cli.menu(submenu_analyse_name, submenu_analyse_options, submenu_analyse_functions)],
            4: lambda: [habit.helper_clear_terminal(), print("Habit Removal Dialog"),
                        [habit.remove(name=cli.validate("name", "name"), safety_ask=cli.validate("choice", "safety"))]],
            9: lambda: [print("Exiting."), habit.database.close_connection(), exit()]}

        # analyse menu definitions
        submenu_analyse_name = "Analyse"

        submenu_analyse_options = {1: "Show all currently tracked habits",
                                   2: "Show all habits with the same periodicity",
                                   3: "Return the longest run streak of all defined habits",
                                   4: "Return the longest run streak for a given habit",
                                   5: "Return the time invested into a given habit",
                                   8: "Return to main menu"}

        submenu_analyse_functions = {1: lambda: [habit.helper_clear_terminal(), habit.analyse("all")],
                                     2: lambda: habit.analyse("all same periodicity",
                                                              argument=cli.validate("periodicity", "periodicity")),
                                     3: lambda: habit.analyse("longest streak of all"),
                                     4: lambda: habit.analyse("longest streak", argument=cli.validate("name", "name")),
                                     5: lambda: habit.analyse("time", argument=cli.validate("name", "name")),
                                     8: lambda: cli.menu(mainmenu_name, mainmenu_options,
                                                         mainmenu_functions)}

        # validation definitions
        cli.validate_functions.update({"name": ["max_length", 20],
                                       "description": ["max_length", 30],
                                       "periodicity": ["daily", "weekly"],
                                       "choice": ["y", "n"],
                                       "number": [0, 1440]})

        # question definitions
        cli.questions.update({"name": ["the habit name", "Any text is valid up to 20 letters"],
                              "description": ["the description of the habit", "Any text is valid up to 30 letters"],
                              "periodicity": ["the periodicity of the habit", "[daily] and [weekly]"],
                              "completed": ["if you completed this habit", "[y]es or [n]o"],
                              "time": ["a time value", "Any number up to 1440 is valid. "
                                                       "This is optional, if you want to skip this enter 0"],
                              "safety": ["if you are sure you want to do this action", "[y]es or [n]o"]})

        # DEV
        # mainmenu_options[5] = "offset time"
        # mainmenu_functions[5] = lambda: habit.manipulate_time(int(input()))
        # mainmenu_options[6] = "current date"
        # mainmenu_functions[6] = lambda: [print(habit.date_today), habit.helper_wait_for_key()]
        # eDEV

        # Ask if sample data should be generated and loaded into the database
        print("Do you want to use sample data and load this database?")
        use_sample_data = cli.validate("choice", "safety")
        if use_sample_data:
            samples = SampleData(31)
            print("Generating habits...")
            samples.create_habits()
            print("Generating events...")
            samples.simulate_events()
            print("Loading Database...")
            habit.database.close_connection()
            habit.database.__init__(samples.db_filename)
            habit.helper_clear_terminal()
            print("Sample data loaded!")
            habit.helper_wait_for_key()

        # Main loop with mainmenu as default
        abort_sequence = False
        while not abort_sequence:
            habit.helper_clear_terminal()
            cli.menu(mainmenu_name, mainmenu_options, mainmenu_functions)

    # If a user presses CTRL + C the database needs to be closed first before exiting, to avoid file locking
    except KeyboardInterrupt:
        print("Got exit key sequence. Closing database connection and exiting.")
        habit.database.close_connection()
        exit()
