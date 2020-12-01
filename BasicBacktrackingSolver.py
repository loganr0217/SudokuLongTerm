from tkinter import *
import time
import random
import matplotlib.pyplot as plt
import csv


class SudokuImage:
    """
    Used for creating a visual representation of a sudoku board
    Displays 9x9 board with colored cells
    Red: incorrect value
    Green: correct value
    White: originally given value
    """
    def __init__(self, master, gameBoard, cboard, bboard):
        global frame
        frame = Frame(master, width=600, height=400)
        frame.pack()

        self.titleLabel = Label(frame, text="Sudoku", borderwidth=2, relief="groove")
        self.titleLabel.grid(row=0, columnspan=10)
        self.CreateGrid(gameBoard)
        self.correctBoard = cboard
        self.baseBoard = bboard

    def update(self, board):
        for r in range(1, 10):
            for c in range(1, 10):
                if board[r-1][c-1] == correctBoard[r-1][c-1] and baseBoard[r-1][c-1] != -1:
                    Label(frame, text=str(board[r-1][c-1]), width=2, height=2, borderwidth=2, relief="solid", bg="green").grid(row=r, column=c, sticky=E)
                elif board[r-1][c-1] == correctBoard[r-1][c-1] and baseBoard[r-1][c-1] == -1:
                    Label(frame, text=str(board[r - 1][c - 1]), width=2, height=2, borderwidth=2, relief="solid").grid(row=r, column=c, sticky=E)
                else:
                    Label(frame, text=str(board[r - 1][c - 1]), width=2, height=2, borderwidth=2, relief="solid", bg="red").grid(
                        row=r, column=c, sticky=E)
    # Function to create the grid of values
    def CreateGrid(self, board):
        for r in range(1, 10):
            for c in range(1, 10):
                Label(frame, text=str(board[r-1][c-1]), width=2, height=2, borderwidth=2, relief="solid").grid(row=r, column=c, sticky=E)

# ^^^ Code for Visual representation ^^^

def FormatBoard(textLetters):
    """
    Takes in sudoku puzzle as string of letters and converts it to a 2-d list
    :param textLetters: sudoku puzzle (string of letters)
    :return: sudoku puzzle (2-d list)
    """

    row, column = (0, 0)
    blankBoard = [[0, 0, 0, 0, 0, 0, 0, 0, 0] for i in range(9)]
    for i in textLetters:
        blankBoard[row][column] = int(i)
        column += 1
        if column == 9:
            column = 0
            row += 1

    return blankBoard

def CheckBoard(board, currentSquare):
    """
    Takes an unsolved board and a square and checks whether there are any duplicates in the square's row, column, or group
    :param board: sudoku board (2-d list)
    :param currentSquare: location of the square being checked
    :return: True if there are no errors and False if any errors are present
    """

    # Check square row and column
    rowValues = set({})
    columnValues = set({})
    row, column = currentSquare
    for k in range(9):
        if board[row][k] in rowValues or board[k][column] in columnValues:
            return False  # error detected
        else:
            if board[row][k] != 0:
                rowValues.add(board[row][k])
            if board[k][column] != 0:
                columnValues.add(board[k][column])

    # Check square 3x3 group
    currentGroupValues = set({})
    i = row // 3
    j = column // 3
    for row in range(i*3, (i*3)+3):
        for column in range(j*3, (j*3)+3):
            if board[row][column] in currentGroupValues:
                return False  # error detected
            else:
                if board[row][column] != 0:
                    currentGroupValues.add(board[row][column])

    return True

def FindZero(board):
    """
    Takes in a sudoku board (solved or unsolved) and finds the first empty square
    :param board: sudoku board (2-d list)
    :return: Location of empty square or 0 if puzzle is complete
    """

    for row in range(9):
        for column in range(9):
            if board[row][column] == 0:
                return (row, column)
    return 0

def SolveBoard(inputBoard, iterator, visualOn, randomAlgorithm=False, sequence=[1,2,3,4,5,6,7,8,9]):
    """
    Takes an unsolved sudoku board and solves it while keeping track of the number of guesses
    :param inputBoard: unsolved sudoku board to be solved
    :param iterator: iterator to keep track of number of guesses made
    :param randomAlgorithm: boolean value which is True if the random sequence is being tested
    :param sequence: sequence of numbers (default is basic [1,2,3,4,5,6,7,8,9]
    :return: Solved sudoku board and number of guesses
    """

    board = [i.copy() for i in inputBoard]
    findZero = FindZero(board)
    if findZero != 0:
        row = findZero[0]
        column = findZero[1]
        sequence = sequence.copy() # Copying sequence to so the argument reference is not being used later

        # If using random algorithm, sequence is shuffled
        if randomAlgorithm == True:
            random.shuffle(sequence)

        # Iterating through each number in the sequence
        for number in sequence:
            iterator += 1
            board[row][column] = number
            if visualOn and iterator % 1000 == 0:
                sudoku.update(board)
                window.update_idletasks()
                window.update()

            check = CheckBoard(board, findZero)
            if check == False and number != sequence[-1]:
                continue
            elif check == False and number == sequence[-1]:
                return [0, iterator]
            else:
                solved, iterator = SolveBoard(board, iterator, visualOn, randomAlgorithm, sequence)

                if solved == 0 and number != sequence[-1]:
                    continue
                elif solved == 0 and number == sequence[-1]:
                    return [0, iterator]
                else:
                    return [solved, iterator]
    else:
        return [board, iterator]

correctBoard = [
[4, 1, 9, 6, 5, 8, 3, 2, 7],
[8, 6, 7, 3, 2, 9, 1, 4, 5],
[5, 3, 2, 7, 1, 4, 6, 9, 8],
[1, 4, 5, 9, 8, 6, 7, 3, 2],
[7, 8, 6, 2, 4, 3, 9, 5, 1],
[2, 9, 3, 1, 7, 5, 4, 8, 6],
[6, 5, 4, 8, 3, 1, 2, 7, 9],
[9, 7, 8, 4, 6, 2, 5, 1, 3],
[3, 2, 1, 5, 9, 7, 8, 6, 4]
]
baseBoard = [
[4, 1, 9, 6, 5, 8, 3, 2, 7],
[-1, -1, 7, -1, -1, 9, 1, 4, 5],
[5, 3, 2, -1, 1, -1, 6, -1, 8],
[-1, 4, -1, 9, -1, 6, -1, 3, 2],
[7, 8, -1, 2, 4, 3, -1, 5, 1],
[2, 9, -1, 1, -1, 5, -1, 8, -1],
[6, -1, 4, -1, 3, -1, 2, 7, 9],
[9, 7, 8, 4, -1, -1, 5, -1, -1],
[3, 2, 1, 5, 9, 7, 8, 6, 4],
]
g = [
[0, 0, 0, 0, 0, 0, 0, 0, 0],
[8, 6, 0, 3, 2, 0, 0, 0, 0],
[0, 0, 0, 7, 1, 4, 0, 9, 0],
[1, 0, 5, 0, 8, 0, 7, 0, 0],
[0, 0, 6, 0, 0, 0, 9, 0, 0],
[0, 0, 3, 0, 7, 0, 4, 0, 6],
[0, 5, 0, 8, 0, 1, 0, 0, 0],
[0, 0, 0, 0, 6, 2, 0, 1, 3],
[0, 0, 0, 0, 0, 0, 0, 0, 0]
]
global sudoku
global window
window = Tk()

# Demonstrating solver with visual
sudoku = SudokuImage(window, g, correctBoard, baseBoard)
sudoku.update(g)
window.update_idletasks()
window.update()
time.sleep(1)
g = SolveBoard(g, 1, 1)[0]
sudoku.update(g)
window.update_idletasks()
window.update()
time.sleep(1)
window.destroy()
# End of visual

numberPuzzles = 100 # Setting for number of puzzles to solve

# Opening csv file with puzzles and extracting data
f = open('sudoku.csv')
csv_f = csv.reader(f)
csvData = list(csv_f)
puzzleTimes = [[], [], []]

visual = False # Visual is off for running analysis
# Running three trials for each type of algorithm
for k in range(3):
    for i in range(numberPuzzles):
        puzzleNumber = random.randint(0, len(csvData) - 1)
        # Original model
        g = FormatBoard(csvData[puzzleNumber][0])

        #tic = time.perf_counter()
        guesses = 0
        g, guesses = SolveBoard(g, guesses, visual)
        #toc = time.perf_counter()
        puzzleTimes[0].append(guesses)

        # Random model
        g = FormatBoard(csvData[puzzleNumber][0])


        #tic = time.perf_counter()
        guesses = 0
        g, guesses = SolveBoard(g, guesses, visual, True)

        #toc = time.perf_counter()

        puzzleTimes[1].append(guesses)

        # Frequency model
        g = FormatBoard(csvData[puzzleNumber][0])

        # Counting number of times each number appears to create frequency based sequence
        freqTable = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
        for j in g:
            for k in j:
                if k != 0:
                    freqTable[k] += 1
        valueList = list(freqTable.values())
        keyList = list(freqTable.keys())
        finalSequence = []
        while len(keyList) > 0:
            if len(keyList) == 1:
                finalSequence.append(keyList.pop(0))
            else:
                minIndex = 0
                for j in range(len(valueList)):
                    if valueList[j] < valueList[minIndex]:
                        minIndex = j
                valueList.pop(minIndex)
                finalSequence.append(keyList.pop(minIndex))

        # tic = time.perf_counter()
        guesses = 0
        g, guesses = SolveBoard(g, guesses, visual, sequence=finalSequence)
        # toc = time.perf_counter()
        puzzleTimes[2].append(guesses)

xValues = [i for i in range(1, numberPuzzles+1)] # Number of puzzles for x-axis

# Making values cumulative to get total number of guesses
for i in range(len(puzzleTimes)):
    for j in range(len(puzzleTimes[i])):
        if j % 100 != 0:
            puzzleTimes[i][j] = puzzleTimes[i][j-1] + puzzleTimes[i][j]

# Lists for averages (commented out when looking at specific trials
origAverage = []
randAverage = []
freqAverage = []
for i in range(numberPuzzles):
    origAverage.append((puzzleTimes[0][i] + puzzleTimes[0][numberPuzzles+i] + puzzleTimes[0][2*numberPuzzles+i])/3)
    randAverage.append((puzzleTimes[1][i] + puzzleTimes[1][numberPuzzles+i] + puzzleTimes[1][2*numberPuzzles+i])/3)
    freqAverage.append((puzzleTimes[2][i] + puzzleTimes[2][numberPuzzles+i] + puzzleTimes[2][2*numberPuzzles+i])/3)
    randAverage[i] = randAverage[i] - origAverage[i]
    freqAverage[i] = freqAverage[i] - origAverage[i]

# Creating figure and subplot for graphs
fig = plt.figure()
ax = fig.add_subplot()

rTotal = 0
fTotal = 0
for i in range(numberPuzzles):
    rTotal += randAverage[i]
    fTotal += freqAverage[i]

rTotal /= numberPuzzles
fTotal /= numberPuzzles
print("Random", rTotal)
print("Frequency:", fTotal)

# Plotting the number of guesses for each algorithm
#ax.plot(xValues, origAverage, "bo-", label="Sequential", markersize=3)
ax.plot(xValues, randAverage, "ro-", label="Random", markersize=3)
ax.plot(xValues, freqAverage, "go-", label="Frequency", markersize=3)

# Setting axis labels and axis limits
plt.ylabel("Number of Guesses")
plt.xlabel("Number of Solved Puzzles")
plt.xlim(left=-10, right=numberPuzzles+10)

# Adding legend, title, and grid to figure before showing the visual
plt.legend()
plt.title("Difference in Guesses from Sequential vs Number of Puzzles Solved")
plt.grid()

# Showing plot
plt.show()