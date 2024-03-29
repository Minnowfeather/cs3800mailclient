from tkinter import *
from tkinter import ttk

# set up 3 state tape
stateTape = ["0","","0"]
tapeIndex = 0
isFreshCalculation = True

#main window
root = Tk()
root.title("Calculator")
root.resizable(False, False)

displayText = StringVar()

def updateText():
    global displayText
    if tapeIndex == 0:
        displayText.set(f"{stateTape[0]}")
    else:
        displayText.set(f"{stateTape[0]} {stateTape[1]} {stateTape[2]}")

def clearTape():
    global stateTape, tapeIndex, isFreshCalculation
    stateTape = ["0","","0"]
    tapeIndex = 0
    isFreshCalculation = True
    updateText()

def evaluate(tape):
    if tape[1] == "/":
        if float(tape[2]) == 0: # prevent division by zero
            return 0
        return float(tape[0]) / float(tape[2])
    elif tape[1] == "*":
        return float(tape[0]) * float(tape[2])
    elif tape[1] == "-":
        return float(tape[0]) - float(tape[2])
    elif tape[1] == "+":
        return float(tape[0]) + float(tape[2])
    print("found nothing")

def processInput(buttonCode):
    global stateTape, tapeIndex, isFreshCalculation
    if tapeIndex == 0:
        if buttonCode.isdigit() == True or buttonCode == ".": # if number is pressed
            if isFreshCalculation: # if this is a fresh calculation (no history)
                stateTape[tapeIndex] += buttonCode
            else: # if number pressed after calculating result
                clearTape()
                stateTape[tapeIndex] = buttonCode
        elif buttonCode != "=":
            tapeIndex = 1 # advance to operator segment
            stateTape[tapeIndex] = buttonCode
    elif tapeIndex == 1: # operator segment of tape
        if buttonCode.isdigit() or buttonCode == ".":
            tapeIndex = 2 # advance to num2 segment
            stateTape[tapeIndex] += buttonCode # num2 = button pressed
        elif buttonCode != "=":
            stateTape[tapeIndex] = buttonCode # change operator
    elif tapeIndex == 2:
        if buttonCode.isdigit() == True or buttonCode == ".": # if number is pressed
            stateTape[tapeIndex] += buttonCode
        else: # if operator pressed
            tapeIndex = 0 # return to 0 index
            stateTape[tapeIndex] = str(evaluate(stateTape)) # evaluate expression and place at num1 slot
            isFreshCalculation = False # prevent from modifying result
            if buttonCode == "=": # if equals pressed
                stateTape[1] = "" # clear rest of tape
                stateTape[2] = "0"
            else: # if non-equals operator pressed
                tapeIndex = 1 # advance to operator slot
                stateTape[tapeIndex] = buttonCode # set operator
                stateTape[2] = "0" # clear num2
    updateText()

# create number display
numberDisplay = Label(root, textvariable=displayText)
numberDisplay.grid(row=0, column=0, sticky="E")
updateText()

# create grid for calculator buttons
grid = ttk.Frame(root, padding="2 2 2 2")
grid.grid(row=1, column=0)

# generate numerical buttons
# note: i generated this with a python script so the formatting is a bit strange
button1 = ttk.Button(grid, text=str(1), command=lambda: processInput(str(1)))
button1.grid(row=3-int(0/3), column=int(0%3))
button2 = ttk.Button(grid, text=str(2), command=lambda: processInput(str(2)))
button2.grid(row=3-int(1/3), column=int(1%3))
button3 = ttk.Button(grid, text=str(3), command=lambda: processInput(str(3)))
button3.grid(row=3-int(2/3), column=int(2%3))
button4 = ttk.Button(grid, text=str(4), command=lambda: processInput(str(4)))
button4.grid(row=3-int(3/3), column=int(3%3))
button5 = ttk.Button(grid, text=str(5), command=lambda: processInput(str(5)))
button5.grid(row=3-int(4/3), column=int(4%3))
button6 = ttk.Button(grid, text=str(6), command=lambda: processInput(str(6)))
button6.grid(row=3-int(5/3), column=int(5%3))
button7 = ttk.Button(grid, text=str(7), command=lambda: processInput(str(7)))
button7.grid(row=3-int(6/3), column=int(6%3))
button8 = ttk.Button(grid, text=str(8), command=lambda: processInput(str(8)))
button8.grid(row=3-int(7/3), column=int(7%3))
button9 = ttk.Button(grid, text=str(9), command=lambda: processInput(str(9)))
button9.grid(row=3-int(8/3), column=int(8%3))
button0 = ttk.Button(grid, text=str(0), command=lambda: processInput(str(0)))
button0.grid(row=4, column=1)

# generate special buttons
buttonDivide = ttk.Button(grid, text="/", command=lambda: processInput("/"))
buttonDivide.grid(row=0, column=3)
buttonMultiply = ttk.Button(grid, text="x", command=lambda: processInput("*"))
buttonMultiply.grid(row=1, column=3)
buttonMinus = ttk.Button(grid, text="-", command=lambda: processInput("-"))
buttonMinus.grid(row=2, column=3)
buttonPlus = ttk.Button(grid, text="+", command=lambda: processInput("+"))
buttonPlus.grid(row=3, column=3)
buttonEquals = ttk.Button(grid, text="=", command=lambda: processInput("="))
buttonEquals.grid(row=4, column=3)
buttonDecimal = ttk.Button(grid, text=".", command=lambda: processInput("."))
buttonDecimal.grid(row=4, column=2)
buttonDivide = ttk.Button(grid, text="C", command=clearTape)
buttonDivide.grid(row=0, column=2)

#enter event loop (makes everything run)
root.mainloop()