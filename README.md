# wordle-bot
A naïve, simple bot for solving Wordle puzzles.

## Description

wordle-bot is a suboptimal, inefficient proprietary aide for solving daily Wordle puzzles. He was programmed in less than a day and purely for fun, and was not made to compete with other [state-of-the-art Wordle solvers](https://freshman.dev/wordle/#/leaderboard).

When tested on `wordle-answers-alphabetical.txt`, wordle-bot had an average win rate of ~98%, and won games in an average of 3.81 turns (high-end bots win on average between 3.421 and 3.550 turns as of time of writing).

## Method & capabilities

wordle-bot starts every game with `SOARE` — although proof exists that `SALET` is a better start, wordle-bot chose `SOARE` for its letter-popularity among accepted answers. The main solving algorithm works by iteratively pruning a word list given the ruleset accumulated by guesses, and selects the most frequently-used word in English out of all potential candidates as the next guess.

This selection method is a not-so-promising heuristic, and I haven't experimented with the method — it might turn out that randomly choosing a candidate is a better approach on average. There are a lot of things that could be explored, for example: when is it better to guess a non-accepted word for the sake of maximum potential pruning? how do we select a candidate that potentially reduces the word list most effectively? etc.

### Playing the game

* `wordle.py` is used only for self-testing of the bot (i.e., word is known)
	* `wordle_tests.py` runs the main function of this file on a word list, and returns statistics
* `wordle_user.py` is for human-assisted games (i.e., real-time)

wordle-bot's guided process is a dialogue between the user and the console, with the user supplying the 5-character hint list returned by Wordle after a guess, with the following encodings:

* `0` signifies a non-match
* `1` signifies an exact match (letter in correct place in word)
* `2` signifies a non-exact match (letter in word but not correct position)

### Example

Today's (27/01/2022) word was `MOUNT`, here's what the input and output looks like with `wordle_user.py`:

```
1	I think	SOARE from 2315 candidates
Guess result: 01000
2	I think	WOULD from 87 candidates
Guess result: 01100
3	I think	YOUNG from 13 candidates
Guess result: 01110
4	I think	COUNT from 2 candidates
Guess result: 01111
5	I think	MOUNT from 1 candidates
```



### Built with

* `numpy` — for arrays and such
* `re` — for pruning word list
* `wordfreq` — for selecting candidate
