import os.path

from cli import Cli
from habit import Habit
from sample_data import SampleData
import cli_habit

if __name__ == "__main__":
    cli = Cli()
    habit = Habit("")

    cli.interactive_mode = True
    habit.user_mode = True
    cli.dev_mode = True

    cli_habit.cli_definitions(cli, habit)

    try:
        # Ask if sample data should be generated and loaded into the database
        print("Do you want to use sample database or your own?")
        use_sample_data = cli.validate("choice", "database")
        if use_sample_data:
            generate_samples = False
            if not os.path.isfile("sample.db"):
                generate_samples = True

            samples = SampleData(31)
            cli.helper_clear_terminal()
            if generate_samples:
                print("Generating habits...")
                samples.create_habits()
                print("Generating events...")
                samples.simulate_events()
                print("Loading database...")
            habit.database.close_connection()
            habit.database.__init__(samples.db_filename)

            print("Sample database loaded!")
            cli.helper_wait_for_key()

            # Main loop with mainmenu as default
            exit_menu: bool = False
            while not exit_menu:
                cli.helper_clear_terminal()
                cli.menu()

    # If a user presses CTRL + C the database needs to be closed first before exiting, to avoid file locking
    except KeyboardInterrupt:
        print("Got exit key sequence. Closing database connection and exiting.")
        habit.database.close_connection()
        exit()
