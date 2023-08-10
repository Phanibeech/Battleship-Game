"""
Battleship Project
Name: Phanindra Gupta
"""


project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4


'''
makeModel(data)
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):
    data["rows"]=10
    data["cols"]=10
    data["Board_Size"]=500
    data["cellsize"]=50
    data["user_ships"]=5
    data["comp_ships"]=5
    data["numShips"]=5
    data["User_Board"]=emptyGrid(10,10) #test.testGrid() 
    data["Comp_Board"]=addShips(emptyGrid(10,10),data["numShips"])
    data["temp_ships"]=[]
    data["user_track"]=0
    data["winner"]=None
    data["max_turns"]=50
    data["current_turns"]=0
    return data
    


'''
makeView(data, userCanvas, compCanvas)
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    drawGrid(data, userCanvas, data["User_Board"], True)
    drawGrid(data, compCanvas, data["Comp_Board"], False)
    drawShip(data,userCanvas,data["temp_ships"])
    drawGameOver(data, userCanvas)
    return


'''
keyPressed(data, events)
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    if event.keysym=="Return":
        makeModel(data)
    return


'''
mousePressed(data, event, board)
Parameters: dict mapping strs to values ; mouse event object ; 2D list of ints
Returns: None
'''
def mousePressed(data, event, board):
    mouse = getClickedCell(data,event)
    if board=="user":
        clickUserBoard(data,mouse[0],mouse[1])
    else:
        runGameTurn(data,mouse[0],mouse[1])
    return

#### WEEK 1 ####

'''
emptyGrid(rows, cols)
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(rows, cols):
    Grid=[]
    for i in range(rows):
        col=[]
        for j in range(cols):
            col.append(1)
        Grid.append(col)
    print(Grid)
    return Grid
    


'''
createShip()
Parameters: no parameters
Returns: 2D list of ints
'''
def createShip():
    row=random.randrange(1,8)
    col=random.randrange(1,8)
    ship=random.randrange(0,1)
    if ship == 0:
        return [[row-1,col],[row,col],[row+1, col]]
    else:
        return [[row,col-1],[row,col],[row,col+1]]
    


'''
checkShip(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    for i in range(len(ship)):
        x=ship[i][0]
        y=ship[i][1]
        if grid[x][y]!=1:
            return False
    return True

'''
addShips(grid, numShips)
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):
    k=0
    while k<numShips:
        ship=createShip()
        if checkShip(grid,ship)==True:
            for i in range(len(ship)):
                x=ship[i][0]
                y=ship[i][1]
                grid[x][y]=2
            k+=1
    return grid


'''
drawGrid(data, canvas, grid, showShips)
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''
def drawGrid(data, canvas, grid, showShips):
    for i in range(data["rows"]):
        for j in range(data["cols"]):
            if grid[i][j]== SHIP_UNCLICKED:
                canvas.create_rectangle(data["cellsize"]*j, data["cellsize"]*i, data["cellsize"]*(j+1), data["cellsize"]*(i+1), fill="yellow")
            elif grid[i][j]==EMPTY_UNCLICKED:
                canvas.create_rectangle(data["cellsize"]*j, data["cellsize"]*i, data["cellsize"]*(j+1), data["cellsize"]*(i+1), fill="pink")
            elif grid[i][j]==SHIP_CLICKED:
                canvas.create_rectangle(data["cellsize"]*j, data["cellsize"]*i, data["cellsize"]*(j+1), data["cellsize"]*(i+1), fill="red")
            elif grid[i][j]==EMPTY_CLICKED:
                canvas.create_rectangle(data["cellsize"]*j, data["cellsize"]*i, data["cellsize"]*(j+1), data["cellsize"]*(i+1), fill="white")
            if grid[i][j]==SHIP_UNCLICKED and showShips==False:
                canvas.create_rectangle(data["cellsize"]*j, data["cellsize"]*i, data["cellsize"]*(j+1), data["cellsize"]*(i+1), fill="pink")
    return


### WEEK 2 ###

'''
isVertical(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):
    ship.sort()
    if ship[0][1]==ship[2][1] and ship [1][1]==ship[2][1]:
        if ship[0][0]==ship[1][0]-1 and ship[2][0]==ship[1][0]+1:
            return True
    return False


'''
isHorizontal(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    ship.sort()
    if ship[0][0]==ship[2][0] and ship[1][0]==ship[2][0] :
        if ship[0][1]==ship[1][1]-1 and ship[2][1]==ship[1][1]+1 :
            return True
    return False


'''
getClickedCell(data, event)
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):
    x=int(event.x/data["cellsize"])
    y=int(event.y/data["cellsize"])
    return [y,x]


'''
drawShip(data, canvas, ship)
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    for i in ship:
        canvas.create_rectangle(data["cellsize"]*(i[1]), data["cellsize"]*(i[0]), data["cellsize"]*(i[1]+1), data["cellsize"]*(i[0]+1), fill="white")
    return


'''
shipIsValid(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    if len(ship)==3:
        if checkShip(grid,ship) and (isVertical(ship) or isHorizontal(ship)):
            return True
    return False


'''
placeShip(data)
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    if shipIsValid(data["User_Board"], data["temp_ships"]):
        for i in data["temp_ships"]:
            data["User_Board"][i[0]][i[1]]=SHIP_UNCLICKED
        data["user_track"]+=1
    else:
        print("error : ship is invalid")
    data["temp_ships"]=[]
    return


'''
clickUserBoard(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    if data["user_track"]==5:
        print("You can start the Game")
        return
    if [row,col] in data["temp_ships"]:
        return
    data["temp_ships"].append([row,col])
    if len(data["temp_ships"])==3:
        placeShip(data)
    return

    


### WEEK 3 ###

'''
updateBoard(data, board, row, col, player)
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    i=data["Comp_Board"]
    j=data["User_Board"]
    if board == i or j:
        if board[row][col]==SHIP_UNCLICKED:
            board[row][col]=SHIP_CLICKED
        elif board[row][col]==EMPTY_UNCLICKED:
            board[row][col]=EMPTY_CLICKED
    if isGameOver(board):
        data["winner"]=player
    return


'''
runGameTurn(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):
    l=getComputerGuess(data["User_Board"])
    m=data["Comp_Board"]
    if m[row][col]==SHIP_CLICKED or m[row][col]==EMPTY_CLICKED:
        return 
    else:
        updateBoard(data,m,row,col,"user")
    updateBoard(data,data["User_Board"],l[0],l[1],"comp")
    data["current_turns"]=data["current_turns"]+1
    if data["current_turns"]==data["max_turns"]:
        data["winner"]="draw"
    return


'''
getComputerGuess(board)
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):
    while True:
        row=random.randint(0,9)
        col=random.randint(0,9)
        if board[row][col]==SHIP_UNCLICKED or board[row][col]==EMPTY_UNCLICKED:


            return[row,col]
    return


'''
isGameOver(board)
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col]==SHIP_UNCLICKED:
                return False
    return True


'''
drawGameOver(data, canvas)
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    if data["winner"]=="user":
        canvas.create_text(250,50, text="Congrats! You won!", fill="black", font=("Times_New_Roman 25 bold"))
        canvas.create_text(300,100, text="Press ENTER to play again!", fill="black", font=("Times_New_Roman 20 bold"))
    if data["winner"]=="comp":
        canvas.create_text(250,50, text="You lost! Try Again!", fill="black", font=("Times_New_Roman 25 bold"))
        canvas.create_text(300,100, text="Press ENTER to play again!", fill="black", font=("Times_New_Roman 20 bold"))
    if data["winner"]=="draw":
        canvas.create_text(250,50, text="It's a Draw! You are out of moves!", fill="black", font=("Times_New_Roman 25 bold"))
        canvas.create_text(300,100, text="Press ENTER to play again!", fill="black", font=("Times_New_Roman 20 bold"))
    return



### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    #test.testGetComputerGuess()
    

    ## Finally, run the simulation to test it manually ##
    runSimulation(500, 500)
    
    
    



    

