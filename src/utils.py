
import tkinter as tk
from typing import List, Tuple, Dict
from tkinter import messagebox

def render_key_frame(parent: tk.Widget, allowed_letters: List[str], Color, key_font=("Helvetica", 10)) -> Tuple[tk.Frame, Dict[str, tk.Label]]:
    key_frame = tk.Frame(parent, bg=Color.LIGHT)
    letter_labels: Dict[str, tk.Label] = {}
    for i, c in enumerate(allowed_letters):
        lbl = tk.Label(
            key_frame,
            text=c,
            bg=Color.NOT_GUESSED,
            fg=Color.DARK,
            width=4,
            height=3,
            font=key_font,
            bd=1,
            relief="raised",
        )
        lbl.grid(row=i // 10, column=i % 10, padx=2, pady=2)
        letter_labels[c] = lbl
    key_frame.pack(pady=5)
    return key_frame, letter_labels


def get_colors_for_status(status, Color) -> Tuple[str, str]:
    name = None
    if status is None:
        name = None
    else:
        name = getattr(status, "name", status)

    mapping = {
        "CORRECT": (Color.CORRECT, Color.LIGHT),
        "WRONG_PLACE": (Color.WRONG_PLACE, Color.LIGHT),
        "WRONG": (Color.WRONG, Color.LIGHT),
        "NOT_GUESSED": (Color.NOT_GUESSED, Color.DARK),
        None: (Color.NOT_GUESSED, Color.DARK),
    }
    return mapping.get(name, (Color.NOT_GUESSED, Color.DARK))


def render_guess_entry_tiles(parent: tk.Widget, allowed_word_length: int, allowed_number_of_guesses: int, Color, entry_font=("Helvetica", 20)) -> Tuple[tk.Frame, List[List[tk.Entry]]]:
    """Create a frame with rows of centered tk.Entry widgets for entering guesses.

    Returns (guesses_frame, guess_entries) where guess_entries is a list of rows,
    each row is a list of tk.Entry widgets. Entries are created disabled by default
    so the caller can enable the active row.
    """
    guesses_frame = tk.Frame(parent, bg=Color.LIGHT)
    guess_entries: List[List[tk.Entry]] = []
    for r in range(allowed_number_of_guesses):
        row_frame = tk.Frame(guesses_frame, bg=Color.LIGHT)
        row_entries: List[tk.Entry] = []
        for c in range(allowed_word_length):
            ent = tk.Entry(
                row_frame,
                width=2,
                font=entry_font,
                justify="center",
                borderwidth=1,
                relief="solid",
                highlightthickness=0,
                bg=Color.LIGHT,
                fg=Color.DARK,
                insertbackground=Color.DARK,
            )
            # ensure disabled appearance matches enabled appearance until submission
            ent.config(disabledbackground=Color.LIGHT, disabledforeground=Color.DARK)
            ent.config(state="disabled")
            ent.pack(side="left", padx=2, pady=2)
            row_entries.append(ent)
        row_frame.pack(pady=2)
        guess_entries.append(row_entries)
    guesses_frame.pack(pady=5)
    return guesses_frame, guess_entries


def validate_input(text: str, max_length: int = 5) -> bool:
    return len(text) <= max_length


def validate_guess(guess: str, allowed_letters: List[str], dictionary: List[str], allowed_word_length: int) -> bool:
    for char in guess:
        if char not in allowed_letters:
            messagebox.showinfo("Ugyldig bokstav", f"Bokstaven '{char}' er ikke tillatt.")
            return False
    if guess not in dictionary:
        messagebox.showinfo("Ugyldig ord", "Ordet finnes ikke i ordboken.")
        return False
    return len(guess) == allowed_word_length