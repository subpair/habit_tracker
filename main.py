"""Startup of the application, including initialization of the cli and habit objects that are used."""
from os import path
from cli import Cli
from habit import Habit
from sample_data import SampleData
from cli_habit import cli_definitions

if __name__ == "__main__":
    cli = Cli()
    habit = Habit()

    # Cli interactive mode means it will use helpers for clearing the terminal and "wait for key".
    cli.interactive_mode = True
    # Habit user mode means the date is updated on every create/update call.
    habit.user_mode = True

    # Load all definitions for the interactive mode
    cli_definitions(cli, habit)

    try:
        # Ask if sample data should be generated and the application loaded into the sample database
        print("Do you want to use a sample database or your own?")
        use_sample_data = cli.validate("choice", "database")
        if use_sample_data:
            GENERATE_SAMPLES = False
            # Only generate new sample data if the database was not created yet
            if not path.isfile("sample.db"):
                GENERATE_SAMPLES = True
            samples = SampleData(31)
            cli.helper_clear_terminal()
            if GENERATE_SAMPLES:
                print("Generating habits...")
                samples.create_habits()
                print("Generating events...")
                samples.simulate_events()
                print("Loading database...")
            # Reset the connection to use the sample database instead of the default one
            habit.database.close_connection()
            habit.database.file_name = "sample.db"
            habit.database.open_connection()
            print("Sample database loaded!")
            cli.helper_wait_for_key()

        # Main loop with mainmenu as default
        exit_menu: bool = False
        while not exit_menu:
            cli.helper_clear_terminal()
            cli.menu()

    # If a user presses CTRL + C the database needs to be closed first before exiting, this avoids file locking.
    except KeyboardInterrupt:
        print("Got exit key sequence. Closing database connection and exiting.")
        habit.database.close_connection()
        exit()
