import random
import string
import csv
import typer
from rich import print
from rich.console import Console
from rich.prompt import Prompt


app = typer.Typer()


class LetterAlreadyGuessedError(Exception):
    pass


class HangmanGame:
    def __init__(self, word: str, max_guesses: int, word_hint: str = None) -> None:
        self.word = word
        self.word_hint = word_hint
        self.guesses = set()
        self.num_guesses = 0
        self.max_guesses = max_guesses

    def guess(self, letter: str) -> None:
        letter = letter.lower()
        if not self.has_remaining_guesses:
            raise AssertionError("Cannot guess when out of guesses")

        if letter in self.guesses:
            raise LetterAlreadyGuessedError(letter)

        self.guesses.add(letter)
        if letter not in self._word_matching:
            self.num_guesses += 1

    @property
    def _word_matching(self):
        return self.word.lower()

    def letter_is_correct(self, letter: str) -> bool:
        return letter.lower() in self._word_matching

    @property
    def masked_word(self):
        # Print as is with capitalization
        if self.has_guessed_word:
            return self.word

        # convert to masked word
        masked_word = []
        for letter in self.word:
            letter = letter.lower()
            if letter not in string.ascii_lowercase or letter.lower() in self.guesses:
                masked_word.append(letter)
            else:
                masked_word.append("_")

        return "".join(masked_word)

    @property
    def has_remaining_guesses(self):
        return self.num_guesses < self.max_guesses

    @property
    def has_guessed_word(self):
        return all(
            l in self.guesses or l not in string.ascii_letters
            for l in self._word_matching
        )

    def is_done(self) -> bool:
        return not self.has_remaining_guesses or self.has_guessed_word


def display_state(game: HangmanGame, action: str) -> None:
    # Parse action
    with_hint = False
    invalid_input = False
    if action is not None:
        if action == "hint":
            with_hint = True
        elif (
            len(action) == 1
            and action in string.ascii_lowercase
            and action not in game.guesses
        ):
            # Make move
            game.guess(action)
        else:
            # Invalid action
            invalid_input = True

    # Game is completed
    if game.is_done():
        if game.has_guessed_word:
            print(f"[bold green]you guessed: {game.word}![/bold green]")
        else:
            print(f"[bold red]You did not guess: {game.word}[/bold red]")
    else:
        # Print state
        print(
            f"Try to guess word: {game.masked_word} [{game.num_guesses} / {game.max_guesses}]"
        )
        if with_hint:
            print(f"Hint: {game.word_hint}")
        elif invalid_input:
            print("[bold red]Invalid input - try again.[/bold red]")


def get_user_action(game: HangmanGame) -> None:
    letters_styled = []
    for letter in sorted(game.guesses):
        if game.letter_is_correct(letter):
            letters_styled.append(f"[green]{letter}[/green]")
        else:
            letters_styled.append(f"[red]{letter}[/red]")

    guesses_str = ",".join(letters_styled)
    letter = Prompt.ask(f"Letter [[bold]{guesses_str}[/bold]]?")
    return letter


def run_guess_game(max_guesses: int, guess_words: bool, guess_phrases: bool):
    def setup_game():
        with open("words.csv", mode="r") as f:
            word_types = []
            if guess_words:
                word_types.append("0")
            if guess_phrases:
                word_types.append("1")

            reader = csv.reader(f)
            all_words = [
                (word, definition)
                for word_type, word, definition in reader
                if word_type in word_types
            ]
            word, definition = random.choice(all_words)

        game = HangmanGame(word=word, word_hint=definition, max_guesses=max_guesses)
        return game

    console = Console()
    game = setup_game()
    console.clear()

    display_state(game, None)
    action = None
    while not game.is_done():
        action = get_user_action(game)
        console.clear()
        display_state(game, action)


@app.command()
def guess(
    mistakes: int = 5,
    words: bool = True,
    phrases: bool = True,
):
    if not (words or phrases):
        raise typer.BadParameter("Must include at least one of words and phrases")
    run_guess_game(max_guesses=mistakes, guess_words=words, guess_phrases=phrases)


def main():
    app()


if __name__ == "__main__":
    main()
