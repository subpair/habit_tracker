"""Unittest for cli."""
from sys import setrecursionlimit
from cli import Cli


class TestCli:
    """Test class for cli tests."""
    def setup_method(self) -> None:
        """Initialize the cli with a new option choice which allows the answers yellow or red."""
        self.cli = Cli()
        self.cli.validate_functions.update()
        self.cli.validate_functions.update({"choice": ["yellow", "red"]})
        self.cli.questions.update({"color": ["which color do you rather like", "[yellow] or [red]"]})

    def test_validation(self, monkeypatch) -> None:
        """Test the validator if he outputs the correct answers and their types."""
        monkeypatch.setattr('builtins.input', lambda _: "test")
        assert self.cli.validate("text", "text") == "test"

        monkeypatch.setattr('builtins.input', lambda _: "yellow")
        assert self.cli.validate("choice", "color") is True

        monkeypatch.setattr('builtins.input', lambda _: "1")
        assert self.cli.validate("number", "number") == 1

    def test_menu(self, monkeypatch) -> None:
        """
        Test the menu by using the default built in "show menu" with a set recursion limit as this goes infinite when
        using the same value every time.

        """
        monkeypatch.setattr('builtins.input', lambda _: "0")
        setrecursionlimit(99)
        try:
            self.cli.menu()
        except RecursionError:
            pass

    def test_helper(self, monkeypatch) -> None:
        """Test the helper "wait for key" if he proceeds after a key was pressed"""
        monkeypatch.setattr('builtins.input', lambda _: "")
        self.cli.helper_wait_for_key()

    def teardown_method(self) -> None:
        """
        Can be used to test the clear terminal helper, commented out by default for the reason it clears all output
        which might be needed for precise unit-testing with output enabled.

        """
        # self.cli.helper_clear_terminal()
        pass
