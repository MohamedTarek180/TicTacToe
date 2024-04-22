from random import randint
from tkinter import *
from tkinter import messagebox


# board structure is made with a dict, index from 1 to 9 indicating positions on the board
# all positions are empty
board = {1: " ", 2: " ", 3: " ",
         4: " ", 5: " ", 6: " ",
         7: " ", 8: " ", 9: " "}

# ai playes with X "maximizing"
# player playes with O "minimizing"
ai = "X"
player = "O"
first = True

# function to draw the board
def drawBoard(board):
    print('')
    for i in range(1, 9, 3):
        for j in range(i, i + 3):
            print('[' + board[j] + ']', end=" ")
        print('\n', end="")


# functions to check if a position is empty or no
def isEmpty(pos):
    if board[pos] == " ":
        return True
    else:
        return False


# function to check if it is a draw
def checkDraw():
    for key in board:
        if board[key] == " ":
            return False
    return True


# function to check for win, it returns a dict i.e. {0: True, 1: 'X'}
# which means there is a win and 'X' is the winner
# index 0 True or False (win or no win), index 1 winner ('X' or 'O' or None)
def checkWin():
    for i in range(1, 9, 3):  # Check horizontal
        if board[i] == board[i + 1] == board[i + 2] and board[i] != " ":
            return {0: True, 1: board[i], 2: [i, i+1, i+2]}
    for i in range(1, 4):  # Check Vertical
        if board[i] == board[i + 3] == board[i + 6] and board[i] != " ":
            return {0: True, 1: board[i], 2: [i, i+3, i+6]}
    if board[1] == board[5] == board[9] and board[1] != " ": #check diagonal 1
        return {0: True, 1: board[1], 2: [1, 5, 9]}
    elif board[3] == board[5] == board[7] and board[3] != " ": #check diagonal 2
        return {0: True, 1: board[3], 2: [3, 5, 7]}
    else:
        return {0: False, 1: None, 2: None}


# insert a letter 'X' or 'O' at position
def insertPos(letter, pos):
    if isEmpty(pos):
        board[pos] = letter
        drawBoard(board)

        # check for win after inserting
        if checkWin()[0]:
            if checkWin()[1] == "X":
                print("Ai wins")
                # exit()
            else:
                print("player wins")
                # exit()
        if checkDraw():
            print("Tie!")
            # exit()
        return
    else:  # if the provided position is not empty, re-enter position
        print("position is not empty")
        pos = int(input("enter another position: "))
        insertPos(letter, pos)
        return


def minimax(board, depth, isMaximizing):
    if checkWin()[1] == ai:
        return 100
    elif checkWin()[1] == player:
        return -100
    elif checkDraw():
        return 0

    if isMaximizing:
        bestScore = -1000

        for key in board:
            if board[key] == " ":
                board[key] = ai
                score = int(minimax(board, depth + 1, False))
                board[key] = " "
                if score > bestScore:
                    bestScore = score
        return bestScore

    else:
        bestScore = 1000

        for key in board:
            if board[key] == " ":
                board[key] = player
                score = int(minimax(board, depth + 1, True))
                board[key] = " "
                if score < bestScore:
                    bestScore = score
        return bestScore


def playerMove(pos):
    insertPos(player, pos)
    return


def aiMove():
    global first
    bestScore = -1000
    bestMove = 0

    if first: #first AI move will be random
        rand = randint(1, 9)
        board[rand] = ai
        score = int(minimax(board, 0, False))
        board[rand] = " "
        first = False
        if score > bestScore:
            bestScore = score
            bestMove = rand
    else:
        for key in board:
            if board[key] == " ":
                board[key] = ai
                score = int(minimax(board, 0, False))
                board[key] = " "
                if score > bestScore:
                    bestScore = score
                    bestMove = key

    insertPos(ai, bestMove)
    return bestMove


#Using tkinter to make GUI
root = Tk()
root.title('Tic-Tac-Toe')


def disable_all_buttons(): # disable all the buttons except reset
    b1.config(state=DISABLED)
    b2.config(state=DISABLED)
    b3.config(state=DISABLED)
    b4.config(state=DISABLED)
    b5.config(state=DISABLED)
    b6.config(state=DISABLED)
    b7.config(state=DISABLED)
    b8.config(state=DISABLED)
    b9.config(state=DISABLED)

def enable_all_buttons(): #enables all buttons
    b1.config(state=NORMAL)
    b2.config(state=NORMAL)
    b3.config(state=NORMAL)
    b4.config(state=NORMAL)
    b5.config(state=NORMAL)
    b6.config(state=NORMAL)
    b7.config(state=NORMAL)
    b8.config(state=NORMAL)
    b9.config(state=NORMAL)
    br.config(state=NORMAL)


# Check to see if someone won
def checkifwon():
    global winner
    winner = False

    if checkWin()[0] == True:
        indxs = checkWin()[2]
        for i in range(3):
            btn[indxs[i]].config(bg="red")

        winner = True
        if checkWin()[1] == "X":
            messagebox.showinfo("Tic Tac Toe", "Ai Wins!!")
        else:
            messagebox.showinfo("Tic Tac Toe", "Player Wins!!")
        disable_all_buttons()
        return True

    # Check if tie
    if checkDraw():
        messagebox.showinfo("Tic Tac Toe", "It's A Draw!")
        disable_all_buttons()
        return False


# Button clicked function
def b_click(b, i):

    if b["text"] == " " :
        playerMoveGUI(i)
        if checkifwon():
            pass
        else:
            aiMoveGui()
            checkifwon()

    else:
        messagebox.showerror(
            "Tic Tac Toe",
            "Pick Another Box",
        )

def startClick(btn0):#function of the start button
    enable_all_buttons()
    aiMoveGui()
    btn0.config(state=DISABLED)



def getPos(index):
    return board[index]


# Start the game over!
def reset():
    global b1, b2, b3, b4, b5, b6, b7, b8, b9, b0, br

    # Build our buttons
    b1 = Button(
        root,
        text=getPos(1),
        font=("times new roman", 20),
        height=3,
        width=6,
        bg="Grey",
        command=lambda i=1: b_click(b1, i),
        name="1",
    )
    b2 = Button(
        root,
        text=getPos(2),
        font=("times new roman", 20),
        height=3,
        width=6,
        bg="Grey",
        command=lambda i=2: b_click(b2, i),
        name="2",
    )
    b3 = Button(
        root,
        text=getPos(3),
        font=("times new roman", 20),
        height=3,
        width=6,
        bg="Grey",
        command=lambda i=3: b_click(b3, i),
        name="3",
    )

    b4 = Button(
        root,
        text=getPos(4),
        font=("times new roman", 20),
        height=3,
        width=6,
        bg="Grey",
        command=lambda i=4: b_click(b4, i),
        name="4",
    )
    b5 = Button(
        root,
        text=getPos(5),
        font=("times new roman", 20),
        height=3,
        width=6,
        bg="Grey",
        command=lambda i=5: b_click(b5, i),
        name="5",
    )
    b6 = Button(
        root,
        text=getPos(6),
        font=("times new roman", 20),
        height=3,
        width=6,
        bg="Grey",
        command=lambda i=6: b_click(b6, i),
        name="6",
    )

    b7 = Button(
        root,
        text=getPos(7),
        font=("times new roman", 20),
        height=3,
        width=6,
        bg="Grey",
        command=lambda i=7: b_click(b7, i),
        name="7",
    )
    b8 = Button(
        root,
        text=getPos(8),
        font=("times new roman", 20),
        height=3,
        width=6,
        bg="Grey",
        command=lambda i=8: b_click(b8, i),
        name="8",
    )
    b9 = Button(
        root,
        text=getPos(9),
        font=("times new roman", 20),
        height=3,
        width=6,
        bg="Grey",
        command=lambda i=9: b_click(b9, i),
        name="9",
    )

    b0 = Button(
        root,
        text="Start",
        font=("times new roman", 20),
        height=3,
        width=6,
        bg="blue",
        command=lambda i=0: startClick(b0),
    )
    br = Button(
        root,
        text="Restart",
        font=("times new roman", 20),
        height=3,
        width=6,
        bg="blue",
        command=lambda i=0: play_again(),
    )

    global btn
    btn = {1: b1, 2: b2, 3: b3, 4: b4, 5: b5, 6: b6, 7: b7, 8: b8, 9: b9}

    # Grid our buttons to the screen
    b1.grid(row=1, column=0)
    b2.grid(row=1, column=1)
    b3.grid(row=1, column=2)
    b4.grid(row=2, column=0)
    b5.grid(row=2, column=1)
    b6.grid(row=2, column=2)
    b7.grid(row=3, column=0)
    b8.grid(row=3, column=1)
    b9.grid(row=3, column=2)
    b0.grid(row=0, column=0)
    br.grid(row=0, column=2)
    disable_all_buttons()

def updatePos(): #update text on buttons
    b1["text"] = getPos(1)
    b2["text"] = getPos(2)
    b3["text"] = getPos(3)
    b4["text"] = getPos(4)
    b5["text"] = getPos(5)
    b6["text"] = getPos(6)
    b7["text"] = getPos(7)
    b8["text"] = getPos(8)
    b9["text"] = getPos(9)


def aiMoveGui():
    aiMove()
    updatePos()


def playerMoveGUI(i):
    playerMove(int(i))
    updatePos()

def play_again():
    global first
    reset()
    for key in board:
        board[key] = " "
    first = True
    updatePos()
    startClick(b0)


reset()

root.mainloop()