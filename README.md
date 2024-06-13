# Sudoku game and slover

## Project describtion

Sudoku game with graphical user interface based on solving Sudoku puzzles, importing new puzzles from files and images, creating new puzzles, and providing a preview of solutions for each puzzle.

## Features

- **User Authentication**: Enable users to register accounts and securely log in to personalize their Sudoku experience.
- **Sudoku Game**: Solve Sudoku puzzles of varying difficulties. Features include providing step-by-step solutions and validating user-inputted solutions for correctness.
- **Save and Resume**: Allow users to save their current Sudoku puzzles and resume them later. Features include saving current puzzle state, including user progress and solution state, and resuming puzzles from where users left off.
- **Time Tracking**: Track solving times for Sudoku puzzles.
- **Database Integration**: Connect the application to a database for user profile management and puzzle storage. Features include securely storing user profiles, saved puzzles, and solving times
- **Hints**: Provide users with hints during puzzle solving if they push the right button
- **File-Based Sudoku Import**: Allow users to import Sudoku puzzles from text files (.txt)
- **Image-Based Sudoku Input (OpenCV)**: Enable users to input Sudoku puzzles from images using OpenCV.
- **Custom Sudoku Creation**: Provide tools for users to create their own Sudoku puzzles.
- **Backtracking Algorithm for Solving**: Implement a backtracking algorithm to solve Sudoku puzzles.
- **GUI**: All of the features have GUI created in PySide6

## Examples

### Login or register

You can login or register a user by typing a username that was not created before

### Menu

You can pick from any sudoku that is added, you can sord them by id, difficulty, last saved date etc

### Adding sudoku

You can choose from 3 options adding from file, picture or creating sudoku by yourself

### Adding sudoku from file

You can choose from all of the txt files in your system. The application checks if its valid and then you can edit it in editor and save to database

### Adding sudoku from picture

You can choose from all of the pictures in your system. The application will find the contours of the sudoku using OpenCV and then determine the numbers using tensorflow. It will check if its valid and then you can edit it in editor and save to database

### Creating sudoku

You can create sudoku using special GUI and then add it to database

### Hints

All of the sudoku have the option to get a hint if a user is stuck and cant get and answer, they can get a random hint by pushing a button or they can get personalized hint by pressing enter in a cell

### Winning :D

## Instalation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/mikolaj-olesinski/Sudoku-game-and-solver
   cd Sudoku-game-and-solver
   ```

2. **Run the installation script**:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

##Project Overview
