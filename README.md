# Norwegian wordle in python

Install dependencies

Run:
```
pip install -r requirements.txt
```

Run the game

```
python3 src/run.py
```

A new word is selected at random each day.

The dictionary is the space separated text file `ord`. Currently this is a list of five letter Norwegian words. 


## Future Work

- Should freeze all other cells in the same row while typing. That is, users can only move left using backspace.
- Show a "Success" message when the correct word is guessed
- Further animatiosn (i.e. when tapping enter, a cell should flupp/shake) such as wordle 
- Add animations (i.e. flipping tiles when guessing, shaking on invalid or incorrect submissions) to mirror Wordle
- Add tests for loading dictionary and seleciton of todays word
