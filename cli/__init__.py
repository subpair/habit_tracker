"""Cli module for handling user input and validating these."""
from os import system
from typing import Union, Tuple, Optional
from datetime import datetime, date


class Cli:
    """The Cli class consist of a validation, a menu method and two helpers (wait-for-key and clear-terminal)."""

    # Validation Method
    # This method has 2 properties, a validation function/a type to validate and validation questions
    #
    # Validation functions
    # - validate_functions dictionary {string or integer, string or integer or [list of strings and/or integers]}
    # The first parameter is used to define the naming of the option pool for identification.
    # The second parameter defines the options it accepts, which can be either use the predefined conventions or be a
    # pool of strings to compare
    # There are 4 predefined special naming identifiers, which can be used to further specify the validation process:
    #   -choice : only allows one option, either option_one and option_two
    #   -number : allows a number between a range of option_one and option_two
    #   -date   : allows a valid date in form of YYYY-MM-DD
    #   -any : accepts any text input
    #   If a number is used a range(from,to) needs to be defined of which numbers are allowed
    # There is also 1 predefined special identifier for the first option parameter:
    #   -max_length : allows a text with a defined maximum length of option_two
    #   this is needed as some text might have a max length defined, but we want different of these validators where
    #   e.g. name is allowed only 20 letters, but a description can have up to 40
    # On an invalid input the user will be re-asked until he enters a valid input
    #
    #   Example:
    #   validate_functions.update({"choice": ["yellow", "red"],
    #                         "some words": ["works", "working", "work", "worked"],
    #                         "tag": ["max_length", 5]})
    #   The first option can be accessed by its name "choice" and will validate user input if it matches either yellow
    #   or red.
    #   The second option "some words" will validate the user input until it matches on of the words.
    #   The third option "tag" will allow any input up to a maximum length of 5

    # Questions
    # - questions dictionary {string or number, list[string, string]}
    # The first parameter is an identifier with which the question are called.
    # The second parameter will be printed out the user in the form of "Please enter %text%." , where %text% is the
    # first object in the list and next to it will be "The options are : %text2%" , where %text2% is the second object
    # in the list
    #
    #   Example:
    #   questions.update({"color": ["which color do you rather like", "[yellow] or [red]"]})
    #   Will ask the User "Please enter which color do you rather like? Available options are: [yellow] or [red]"
    # Both can be mixed - there can be any validator used with any question

    def __init__(self) -> None:
        """
        Initialize basic objects for the validator.

        The basic objects consist of a dictionary for functions with the identifier item "text" and a question object
        with the identifier item "text" in it.

        Example Usage: cli.validate("text", "text") will validate input of text and check if it only contains numerical
        and/or alphabetical content.

        the variable interactive_mode is used to control if the helpers (wait-for-key and clear-terminal) are used.

        """
        self.validate_functions: dict = {"text": "any",
                                         "choice": ["y", "n"],
                                         "number": [0, 1440],
                                         "date": ["date"]}
        self.questions: dict = {"text": ["something", "Any text is valid"],
                                "choice": ["a choice out of two options", "[y]es or [n]o"],
                                "number": ["a number out of a range", "between 0 and 1440"],
                                "date": ["a date", "a valid date"]}
        self.interactive_mode: bool = True

        # Menu Builder
        # The Menu consist of:
        # - %name%_menu_name string ""
        # contains the name of the menu
        #
        # - %name%_menu_options dictionary {integer, string}
        # holds the number with which the option can be chosen and a description of this option
        #
        # - %name%menu_functions dictionary {integer, lambda: function or list of functions in order}
        # connects the number of the menu_options with a functionality, which is called through a lambda function
        #
        # %name% can be anything, but any menu needs these 3 to have something displayed
        #
        #
        #   Example:
        #       main_menu_name = "first"
        #       main_menu_options.update({5: "Print Hello world"})
        #       main_menu_functions.update({5: lambda: [print("Hello "), print("world")]})
        #       This will override the default menu name and add a new function to the menu, which will print 2 times a
        #       string when the number 5 is chosen

        self.main_menu_name: str = "main"
        self.main_menu_options: dict = {0: "Show menu"}
        self.main_menu_functions: dict = {0: lambda: self.menu()}

        self.message_error = "An unknown error occurred. Please copy the previous output and send it to developer."

    def validate(self, validation_type: str, question_object: str) -> Union[bool, str, int, date]:
        """
        Validate the user input.

        It validates by the combination of the type of input and the objects this type allows.

        The loop will re-ask the user if he gave a wrong answer until he gives the correct answer.

        :param validation_type: str the type of the input, this can be any defined option of validate_functions
        :param question_object:  str he questions that will be asked, this can be any defined option of questions
        :return: validated input of the user in the needed format, choice will give a bool of True or False, number will
         give an int number, date will give a date and all other will return a str
        """
        if validation_type in self.validate_functions:
            option_identifier = self.validate_functions[validation_type][0]
            options = self.validate_functions[validation_type]
            option_one = self.validate_functions[validation_type][0]
            option_two = self.validate_functions[validation_type][1]
        else:
            raise Exception(str(validation_type) + " has no validation function")

        if question_object in self.questions:
            question_type = self.questions[question_object][0]
            questions_options = self.questions[question_object][1]
        else:
            raise Exception(str(question_object) + " has no validation question")

        # Validation loop start
        validation_input: Union[str, int, bool, date] = ""
        valid_input: bool = False
        while not valid_input:
            print("Please enter {question_type}.\nAvailable options are: {questions}."
                  .format(question_type=question_type, questions=questions_options))
            validation_input = input(">")
            if len(validation_input) < 80:
                validation_input_no_whitespaces = validation_input.replace(" ", "")
                if validation_input_no_whitespaces.isalnum():
                    # Allow only a choice between two options
                    if validation_type.casefold() == "choice":
                        valid_input, validation_input = self.validate_choice(validation_input, option_one, option_two)
                    # Allow only numbers between a range of two options
                    elif validation_type.casefold() == "number":
                        valid_input, validation_input = self.validate_number(validation_input, option_one, option_two)
                    # Allow only text with a defined max length
                    elif option_identifier == "max_length":
                        if len(validation_input) > option_two:
                            print("The text is too long!\nPlease reduce the number to the allowed "
                                  "{allowed_text_length}!".format(allowed_text_length=option_two))
                        else:
                            valid_input = True
                    # Generic option that accepts every input
                    elif validation_input.casefold() in options or options == "any":
                        valid_input = True
                    else:
                        print("The option you entered is not valid!")
                elif validation_input == "":
                    print("You entered nothing!\nPlease type at-least something!")
                elif validation_type.casefold() == "date":
                    valid_input, validation_input = self.validate_date(validation_input)
                else:
                    print("Your input contains an invalid character!\nPlease input only text without additional "
                          "characters!")
            else:
                print("The text you entered is too long!\nPlease reduce it!")
        return validation_input

    @staticmethod
    def validate_choice(user_input: str, option_one: str, option_two: str) \
            -> Tuple[bool, bool]:
        """
        Check the input string if it is one of the both available options.

        :param user_input: str of user input
        :param option_one: str of option one
        :param option_two: str of option two
        :return: tuple of [bool] if input is valid and [bool] of True if validation_input is option_one or False if it
        is option_two
        """
        validation_input = False
        if user_input.casefold() == option_one:
            validation_input = True
            valid_input = True
        elif user_input.casefold() == option_two:
            validation_input = False
            valid_input = True
        else:
            print("This is not a valid answer!")
            valid_input = False
        return valid_input, validation_input

    @staticmethod
    def validate_number(user_input: str, option_one: int, option_two: int) \
            -> Tuple[bool, int]:
        """

        Check the input string if it is a number in the range between or exactly one of the both available options.

        :param user_input: str of user input
        :param option_one: int of option one / begin of range
        :param option_two: int of option two / end of range
        :return: tuple of [bool] if input is valid and [int] of the number from validation_input if it is in range of or
         exactly option_one and/or option_two
        """
        validation_input = 0
        if user_input.isnumeric():
            validation_number = int(user_input)
            if option_one <= validation_number <= option_two:
                validation_input = validation_number
                valid_input = True
            else:
                print("This number is too high!\nPlease reduce it to a number between "
                      "{number_lower_limit} and {number_upper_limit}!"
                      .format(number_lower_limit=option_one, number_upper_limit=option_two))
                valid_input = False
        else:
            print("This is not a valid number!\nPlease enter a valid Number!")
            valid_input = False
        return valid_input, validation_input

    @staticmethod
    def validate_date(user_input: str) \
            -> Tuple[bool, date]:
        """
        Check the input string if it is a date in the correct format.

        :param user_input: str of user input
        :return: tuple of [bool] if input is valid and [date] of the input from the user if it is a date in the format
         "YYYY-MM-DD"
        """
        date_format: str = "%Y-%m-%d"
        validation_input = date.today()
        try:
            validation_date = datetime.strptime(user_input, date_format).date()
            validation_input = validation_date
            valid_input = True
        except ValueError:
            print("This is not a valid date!\nPlease enter a valid date!")
            valid_input = False
        return valid_input, validation_input

    def menu(self, menu_name: Optional[str] = None, menu_options: Optional[dict] = None,
             menu_functions: Optional[dict] = None) -> None:
        """
        Menu that is created via the parameters and loops until an associated option is found.

        :param menu_name: str the name text of the menu to be displayed
        :param menu_options: dict of the options the menu does have
        :param menu_functions: dict The functions for the menu options
        """
        if menu_name is None:
            menu_name = self.main_menu_name
        if menu_options is None:
            menu_options = self.main_menu_options
        if menu_functions is None:
            menu_functions = self.main_menu_functions
        self.helper_clear_terminal()
        print("You are in the {current_menu_name} menu.\nThe options are:"
              .format(current_menu_name=menu_name))
        # Displays all available menu options
        for key, value in sorted(menu_options.items()):
            print(key, value)
        valid_input = False
        while not valid_input:
            menu_input = input(">")
            # Check if it is a number
            if menu_input.isnumeric():
                menu_number = int(menu_input)
                # Check if there is an option and a function for the input number
                if menu_number in menu_options.keys() and menu_number in menu_functions.keys():
                    menu_functions[menu_number]()
                    valid_input = True
                # KeyError menu_options
                elif menu_number not in menu_options.keys():
                    print("There is no option for this number!\nPlease enter the number of an existing option!")
                # KeyError menu_functions
                elif menu_number not in menu_functions.keys():
                    print(
                        "There is currently no function assigned to this option!\nPlease bring the dev some coffee so "
                        "he can add this function :)")
            else:
                print("This was not a number you entered!\nPlease enter a number of an existing option!")

    def helper_wait_for_key(self) -> None:
        """Print text and wait for user input to let the user read the output of his last actions."""
        if self.interactive_mode:
            input("...press enter to continue...\n>")

    def helper_clear_terminal(self) -> None:
        """Clear the terminal for better and clearer visibility."""
        if self.interactive_mode:
            system('cls||clear')
