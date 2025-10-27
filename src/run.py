import tkinter as tk
from collections import Counter
from enum import Enum

from utils import (
    render_guess_entry_tiles,
    render_key_frame,
    validate_guess,
    get_colors_for_status,
)
from tkinter import messagebox

from config import (
    dictionary,
    TODAYS_WORD,
    ALLOWED_LETTERS,
    ALLOWED_WORD_LENGTH,
    ALLOWED_NUMBER_OF_GUESSES,
)

class LetterStatus(Enum):
    WRONG = 0
    WRONG_PLACE = 1
    CORRECT = 2
    NOT_GUESSED = 3

class Color:
    CORRECT = "#2FA452"
    WRONG_PLACE = "#AFA93A"
    WRONG = "grey35"
    NOT_GUESSED = "grey80"
    LIGHT = "white"
    DARK = "black"

# Run the GUI for today's Ordl
def run_todays_ordl():
    attempts = 0
    guessed_letters = dict(
        zip(ALLOWED_LETTERS, [LetterStatus.NOT_GUESSED] * len(ALLOWED_LETTERS))
    )
    window = tk.Tk()
    window.geometry(
        "{}x{}".format(ALLOWED_WORD_LENGTH * 100, 100 * ALLOWED_NUMBER_OF_GUESSES)
    )
    window.configure(bg=Color.LIGHT)
    window.title("Ordl - Dagens ord")

    # Render entry-based guess tiles and make the active row editable
    guesses_frame, guess_entries = render_guess_entry_tiles(
        window, ALLOWED_WORD_LENGTH, ALLOWED_NUMBER_OF_GUESSES, Color
    )

    # helper to enable/disable rows and manage focus/navigation
    def enable_row(row_idx: int):
        row = guess_entries[row_idx]
        for ent in row:
            ent.config(state="normal")
            ent.delete(0, tk.END)
        # focus first entry
        row[0].focus_set()

    # enable first row
    enable_row(0)

    # Render keyboard / key frame using helper. We also get back the mapping letter->Label
    key_frame, letter_labels = render_key_frame(window, ALLOWED_LETTERS, Color)

    # keep the mapping of overall letter statuses for keyboard coloring
    letter_statuses = {c: None for c in ALLOWED_LETTERS}

    # allow Enter key to submit current row
    window.bind("<Return>", lambda e: on_guess())

    def make_key_handler(r, c):
        def handler(event):
            key = event.keysym
            ent = guess_entries[r][c]
            if key == "BackSpace":
                # if empty, move focus back
                val = ent.get().strip()
                if val == "":
                    if c > 0:
                        prev = guess_entries[r][c - 1]
                        prev.config(state="normal")
                        prev.focus_set()
                        prev.delete(0, tk.END)
                else:
                    ent.delete(0, tk.END)
                return
            # ignore control keys
            if len(key) > 1:
                return
            ch = event.char.upper()
            if not ch.isalpha():
                return
            # set value and move focus forward
            ent.delete(0, tk.END)
            ent.insert(0, ch)
            if c + 1 < ALLOWED_WORD_LENGTH:
                nxt = guess_entries[r][c + 1]
                nxt.config(state="normal")
                nxt.focus_set()
        return handler

    # attach key handlers to all entries
    for r, row in enumerate(guess_entries):
        for c, ent in enumerate(row):
            ent.bind("<KeyRelease>", make_key_handler(r, c))

    def on_guess():
        nonlocal attempts
        # check that we have not exceeded ALLOWED_NUMBER_OF_GUESSES
        if attempts >= ALLOWED_NUMBER_OF_GUESSES:
            return

        # build the text from the active row entries
        cur_row = guess_entries[attempts]
        chars = [ent.get().strip().upper() for ent in cur_row]
        text = "".join([c if c else "" for c in chars])

        if len(text) != ALLOWED_WORD_LENGTH:
            messagebox.showwarning("Invalid", "Please fill all letters before submitting.")
            return
        
        if not validate_guess(text, ALLOWED_LETTERS, dictionary, ALLOWED_WORD_LENGTH):
            return

        attempts += 1

        # if not correct, check if we have attempts left
        remaining = ALLOWED_NUMBER_OF_GUESSES - attempts
        if remaining <= 0:
            button.config(state=tk.DISABLED)
            # disable all entries
            for r in range(attempts, ALLOWED_NUMBER_OF_GUESSES):
                for ent in guess_entries[r]:
                    ent.config(state="disabled")

        else:
            nonlocal guessed_letters

            # give feedback on the letter statuses
            status_list = [None] * ALLOWED_WORD_LENGTH
            target_chars = list(TODAYS_WORD)
            for i, ch in enumerate(text):
                if i < len(target_chars) and ch == target_chars[i]:
                    status_list[i] = LetterStatus.CORRECT
                    target_chars[i] = None

            # count remaining target letters
            remaining = Counter([c for c in target_chars if c is not None])

            """ ------GUESS EVALUATION------ """
            # mark present / absent
            for i, ch in enumerate(text):
                if status_list[i] is None:
                    if remaining.get(ch, 0) > 0:
                        status_list[i] = LetterStatus.WRONG_PLACE
                        remaining[ch] -= 1
                    else:
                        status_list[i] = LetterStatus.WRONG

            # Update guess entries with colors and disable them
            row_idx = attempts - 1
            for i, ch in enumerate(text):
                st = status_list[i]
                bg, fg = get_colors_for_status(st, Color)
                ent = guess_entries[row_idx][i]
                ent.config(state="disabled")
                ent.delete(0, tk.END)
                ent.insert(0, ch)
                ent.config(disabledbackground=bg, disabledforeground=fg)

            """ ------KEYBOARD LETTERS LOGIC------ """
            # Update overall letter statuses
            for ch, st in zip(text, status_list):
                prev = letter_statuses.get(ch)
                if prev == LetterStatus.CORRECT:
                    continue
                if st == LetterStatus.CORRECT:
                    letter_statuses[ch] = LetterStatus.CORRECT
                elif st == LetterStatus.WRONG_PLACE:
                    # only upgrade to WRONG_PLACE if we don't already have CORRECT or WRONG_PLACE
                    if prev not in (LetterStatus.CORRECT, LetterStatus.WRONG_PLACE):
                        letter_statuses[ch] = LetterStatus.WRONG_PLACE
                else:  # st == LetterStatus.WRONG
                    if prev is None:
                        letter_statuses[ch] = LetterStatus.WRONG

            # apply colors to keyboard labels
            for c, lbl in letter_labels.items():
                st = letter_statuses.get(c)
                bg, fg = get_colors_for_status(st, Color)
                lbl.config(bg=bg, fg=fg)

            # if the guess is correct, disable further input
            if text == TODAYS_WORD:
                button.config(state=tk.DISABLED)
                # disable remaining rows
                for r in range(attempts, ALLOWED_NUMBER_OF_GUESSES):
                    for ent in guess_entries[r]:
                        ent.config(state="disabled")
                return

            # enable next row if any
            if attempts < ALLOWED_NUMBER_OF_GUESSES:
                enable_row(attempts)

    button = tk.Button(
        window,
        text="Guess",
        width=14,
        command=on_guess,
        bd=0,
        relief="flat",
        bg=Color.NOT_GUESSED,
        fg=Color.DARK,
        font=("Helvetica", 12, "bold"),
        cursor="hand2",
        padx=8,
        pady=8,
        highlightthickness=0,
    )
    button.pack(pady=20)

    window.mainloop()


if __name__ == "__main__":
    run_todays_ordl()
