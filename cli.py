class Cli:
    # The CLI consist of a validation and a menu method

    # User validation functions
    # - validate_functions dictionary {string or integer, string or integer or [list of strings and/or integers]}
    # The first parameter is used to define the naming of the option pool for identification.
    # The second parameter defines the options it accepts, which can be either use the predefined conventions or be a
    # pool of strings to compare
    # There are 3 predefined special naming identifiers, which can be used to further specify the validation process:
    #   -choice : only allows one option, either option_one and option_two
    #   -number : allows a number between a range of option_one and option_two
    #   -any : accepts any text input
    #   If a number is used a range(from,to) needs to be defined of which numbers are allowed
    # There is also 1 predefined special identifier for the first option parameter:
    #   -max_length : allows a text with a defined maximum length of option_two
    #   this is needed as some text might have a max length defined, but we want different of these validators where
    #   e.g. name is allowed only 20 letters, but a description can have up to 40
    #   On an invalid input the user will be re-asked until he enters a valid input
    #
    #   Example:
    #   validate_functions = {"choice": ["yellow", "red"],
    #                         "some words": ["works", "working", "work", "worked"],
    #                         "tag": ["max_length", 5]}
    #   The first option can be accessed by its name "choice" and will validate user input if it matches either yellow
    #   or red.
    #   The second option "some words" will validate the user input until it matches on of the words.
    #   The third option "tag" will allow any input up to a maximum length of 5

    validate_functions = {}
    # User questions
    # - questions dictionary {string or number, list[string, string]}
    # The first parameter is an identifier with which the question are called.
    # The second parameter will be printed out the user in the form of "Please enter %text%." , where %text% is the
    # first object in the list and next to it"The options are : %text2%" , where %text2% is the second object in
    # the list
    #
    #   Example:
    #   questions = {"color": ["which color do you rather like", "[yellow] or [red]"]}
    #   Will ask the User "Please enter which color do you rather like? Available options are: [yellow] or [red]"

    questions = {}

    def validate(self, validation_type: str, question_object: str):
        """
        This function is validating the user input by the combination of the type of input and the objects this
        type allows.\n
        The loop will re-ask the user if he gives a wrong answer until he gives the correct answer\n
        :param validation_type: The type of the input, this can be any defined option of validate_functions
        :param question_object:  The questions that will be asked
        :return: returns the validated input of the user
        """

        valid_input = False
        option_identifier = self.validate_functions[validation_type.casefold()][0]
        options = self.validate_functions[validation_type]
        option_one = self.validate_functions[validation_type][0]
        option_two = self.validate_functions[validation_type][1]
        question_type = self.questions[question_object][0]
        questions_options = self.questions[question_object][1]

        # Validation loop start
        while not valid_input:
            if question_object in self.questions.keys():
                print("Please enter {question_type}. Available options are: {questions}."
                      .format(question_type=question_type,
                              questions=questions_options))
                validation_input = input(">")

                # Allow only a choice between two options
                if validation_type.casefold() == "choice":
                    if validation_input.casefold() == option_one:
                        valid_input = True
                        return True
                    elif validation_input.casefold() == option_two:
                        valid_input = True
                        return True
                    else:
                        print("This is not a valid answer!")
                        valid_input = False
                # Allow only numbers between a range of two options
                elif validation_type.casefold() == "number":
                    if validation_input.isnumeric():
                        validation_input = int(validation_input)
                        if option_one <= validation_input <= option_two:
                            valid_input = True
                            return validation_input
                        else:
                            print("This number is too high! Please reduce it to a number between "
                                  "{number_lower_limit} and {number_upper_limit}!"
                                  .format(number_lower_limit=option_one, number_upper_limit=option_two))
                            valid_input = False
                    else:
                        print("This is not a valid number! Please enter a valid Number!")
                        valid_input = False
                # Allow only text with a defined max length
                elif option_identifier == "max_length":
                    if validation_input == "":
                        print("Please enter something!")
                        valid_input = False
                    else:
                        if len(validation_input) > option_two:
                            print("The text is too long! Please reduce the number to the allowed "
                                  "{allowed_text_length}!"
                                  .format(allowed_text_length=option_two))
                            valid_input = False
                        else:
                            valid_input = True
                            return validation_input
                # Generic option that accepts every input
                elif validation_input.casefold() in options or option_one == "any":
                    if validation_input == "":
                        print("Please enter something.")
                        valid_input = False
                    else:
                        valid_input = True
                        return validation_input
                else:
                    print("Option not possible! The options are : {questions}"
                          .format(questions=questions_options))
                    valid_input = False
            else:
                print("Option not possible! The options are : {questions}"
                      .format(questions=questions_options))

    @staticmethod
    def menu(menu_name: str, menu_options: dict, menu_functions: dict):
        """
        The menu will be created via the parameters and loop until an associated option is found.\n
        :param menu_name: The name text of the menu to be displayed
        :param menu_options: The options the menu does have
        :param menu_functions: The functions for the menu options
        """

        print("You are in the {current_menu_name} menu.\nThe options are:"
              .format(current_menu_name=menu_name))
        # Displays all available menu options
        for key, value in sorted(menu_options.items()):
            print(key, value)
        valid_input = False
        while not valid_input:
            menu_number = input(">")
            # Check if it is a number
            if menu_number.isnumeric():
                menu_number = int(menu_number)
                # Check if there is an option and a function for the input number
                if menu_number in menu_options.keys() and menu_number in menu_functions.keys():
                    menu_functions[menu_number]()
                    valid_input = True
                # KeyError menu_options
                elif menu_number not in menu_options.keys():
                    print("There is no option for this number! Please enter the number of an existing option!")
                # KeyError menu_functions
                elif menu_number not in menu_functions.keys():
                    print(
                        "There is currently not function assigned to this option! Please bring the dev some coffee so "
                        "he can add this function :)")
            else:
                print("Invalid input! Please enter a number for an existing option!")
