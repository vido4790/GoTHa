# GoTHa: Gota group's Treasure Hunt

Good. This means you were able to crack the first and probably the most difficult puzzle: the QR code. As per the instructions in the note accompanying the gifts, hopefully you haven't opened the envelopes yet.

For your ease, a short video that explains GoTHa can be found [here](https://www.youtube.com/watch?v=dQw4w9WgXcQ). But if you really want to read, here you go:

As you may have correctly guessed by this point, you will have to solve a number of puzzles to open the envelopes. There are eight puzzles for the eight envelopes. After solving puzzle number n, you may open the nth envelope.

Only when you submit to the script the correct answer to the current puzzle, will the question for the next one appear.

Since the envelopes themselves aren't locked in anyway, there's nothing preventing you from opening them.
We are relying on your honesty to make sure that you follow these instructions. Or maybe the envelopes are enchanted with a spell that turns you into a frog if you haven't solved that puzzle. Do you really want to test that hypothesis?


## Rules
1. Do not open the envelopes before solving the corresponding puzzles.
2. The code does not perform a string compare to figure out if the answer is correct. That is to say that the code does not contain the answers. As a result, you are free to read and understand any and all of the code. In fact, you are encouraged to do so. You may find some interesting information that way.
3. You may also explore all the contents of all the directories in this repository.
4. Exploring the git history is also a permissible action.
5. Hacking the scripts to find a way around them is also fair game.
6. There may be puzzles that require you to do some coding or at least use a computer to solve them.
7. Using a search engine is allowed.
8. Please do not alter the contents of the folder `resources/data`. Doing so may render the scripts inoperable.
9. The unlocked puzzles can be found in `resources/puzzles` in a directory named with the level number.


## Setup and Requirements

### Requirements
The script requires the following to work correctly:
1. A mac/linux machine. The code is untested on Windows and may not work.
2. Python 2.7
3. pip
4. Packages as specified in `requirements.txt`.
The steps to do so can be found in the [Setup](#setup) section.
5. A brain. (This is important. Solving the puzzles without a brain can be challenging \[citation required\]).

### Setup
1. Clone the git repo
```
$ git clone https://github.com/vido4790/GoTHa.git && cd GoTHa
```
2. Create a virtual environment
```
$ virtualenv venv && source venv/bin/activate
```
3. Install requirements
```
$ pip install -r requirements.txt
```
4. Enjoy!
```
$ python GoTHa.py
```

## How to Create Puzzles
To create the puzzles please follow the following steps:
1. Decide on the number of levels.
2. Create n directories in `resources/inputs` for the n levels. Name each directory with the level number, starting with 1.
3. Create a JSON file with the following format:
```
{
  "1": 
  {
    "ans"         : "<Answer. Must not contain any special characters. All spaces are stripped out.>",
    "pepper"      : "<A pepper string that is used to create the salt. Pepper is subject to the same restrictions as the answer, and must also be less than 128 chars long>"
  },
  .
  .
  .
  "<level number>":
  {
    "ans"         : "<level answer>",
    "pepper"      : "<level pepper.>"
  }
  .
  .
}
```
4. Fill in the answers and the pepper for each of the level.
5. Place the puzzles for each level into the corresponding directory as created in step 2.
6. Execute the following command:
```
$ python GoTHa.py create
```
7. The script should place the appropriate files in the `resources/data` and the `resources/puzzles` directories.
8. The `.gitignore` file is programmed to ignore the contents of `resources/inputs` to prevent from answers being inadvertently revealed. Please be careful as to not push the unencrypted files onto origin.
9. When the encrypted files are ready, please commit and push them to the server.


## Credits
Gota group is responsible for the gifts. The code was written mostly by [Virag Doshi](https://gist.github.com/vido4790). The puzzles were created mostly by [Moumita Dey](https://github.com/mdey6).