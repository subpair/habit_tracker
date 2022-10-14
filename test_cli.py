from sys import setrecursionlimit
from cli import Cli


class Tests:

    def setup_method(self) -> None:
        self.cli = Cli()
        self.cli.validate_functions.update()
        self.cli.validate_functions.update({"choice": ["yellow", "red"]})
        self.cli.questions.update({"color": ["which color do you rather like", "[yellow] or [red]"]})

    def test_validation(self, monkeypatch) -> None:
        monkeypatch.setattr('builtins.input', lambda _: "test")
        assert self.cli.validate("text", "text") == "test"

        monkeypatch.setattr('builtins.input', lambda _: "yellow")
        assert self.cli.validate("choice", "color") is True

        monkeypatch.setattr('builtins.input', lambda _: "1")
        assert self.cli.validate("number", "number") == 1

    def test_menu(self, monkeypatch) -> None:
        monkeypatch.setattr('builtins.input', lambda _: "0")
        setrecursionlimit(99)
        try:
            self.cli.menu()
        except RecursionError:
            pass

    def test_helper(self, monkeypatch) -> None:
        monkeypatch.setattr('builtins.input', lambda _: "")
        self.cli.helper_wait_for_key()

    def teardown_method(self) -> None:
        # self.cli.helper_clear_terminal()
        pass
