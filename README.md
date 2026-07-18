# Museum Night Game

## What it is
It is a simple python game (trivia-like). It has three different levels:
1. Easy level.
2. Medium.
3. Final level. If well it is the last one, it does not mean that it's the hardest one.

For every level it shows a question and three different answers (only one is correct). If the player selects the right one, then the "DEATH" character moves away form the "PACIENT" character (aka the dog). Otherwise, Death takes dog's life, and the player loses. 

At any point the player has one life only and they can win after the last correct question. 

## Historical review
I created this game in order to explain basic medical concepts at Museum Night event. 

First used in 2025 edition. The game was well received by attenders in general. Since they have only one life, it was a nice and healthy quick challenge to take. 

Even though it was designed for that purpose, it does not mean that it cannot be used in any other event. 
## Changes
Now 3rd level has a timer. 
## How to use
First of all, clone the repo and make sure you have UV installed.

### Questions
Every level has its own file with questions (archivo.txt, arch_lvl2.txt, arch_lvl3.txt respectly) and very file must have the same style:
(This is for lvl1 and lvl3 files)
* At the biggining of the file there must be an integer. It means the amount of questions in this file. 
```
<Question_number>
<Question>
<Option1>
<Option2>
<Option3>
*<Question_number>*
<Next_Question_number>
...
```
(this other is for lvl2)
```
<Question_number>
<Question>
<Option1>
<Option2>
<Option3>
<hint1, hint2, ..., hintN>
*<Question_number>*
<Next_Question_number>
```
As you can see, there is no blank space between any pair of lines, and, file for lvl2 is a little bit different: it has the hint section. This was thought to be used as useful (or tricky) hint for the player in order to solve that lvl2 question. Every question in this file must have at least one hint, but (as I said) they can help or not to solve the question.

Option 3 must always be the right one. Don't worry about randomness, the program itself does it for you, but in this .txt files option 3 must always be true.

Change question file as you wish but keep them just where they are (linux_game/)

### Timer
set QUESTION_TIME variable in intento1.py

### Running the game
Being on MuseumNightGame/ run
```bash
uv sync && source .venv/bin/activate && cd linux_gam/ && python3 intento1.py
```

## Important Considerations
First of all, I want to apologize for the directory structure. I started this project very early in my code-learning phase, so I was terrible at deciding how to structure this project. 
Nevertheless, I learned a lot in my path (such as git) and improved the general structure (yes, it was even worst). I decided to keep some of those ugly aspects (such as file names) for personal reasons

Since the game has no story at all, you can use it for a medical trivia or a movie trivia. Its characters are generic enough for any situation