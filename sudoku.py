from tkinter import Tk, Canvas, Frame, Entry, Button, BOTH, TOP, BOTTOM, LEFT, RIGHT, StringVar, OptionMenu
import random
from datetime import datetime, timedelta

MARGIN = 20
SIDE = 50
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9
CELLS_TO_DELETE = 40
grid = [[0]*9 for varr in range(9)]
allowed_cells = [[0]*9 for varr in range(9)]
random_x = list(range(9))
random_y = list(range(9))
random_nos = list(range(1,10))

root = Tk()
root.title('SUDOKU')
my_canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg='white')
my_canvas.pack(fill=BOTH, side=TOP)
sel_r = -1
sel_c = -1
w_r = -1
w_c = -1
vic_flag = False

def randomize():
    global grid, random_x, random_y, random_nos, allowed_cells
    for i in range(9):
        for j in range(9):
            grid[i][j] = 0
            allowed_cells[i][j] = 0
    random_x = list(range(9))
    random_y = list(range(9))
    random_nos = list(range(1,10))
    random.shuffle(random_x)
    random.shuffle(random_y)
    random.shuffle(random_nos)
    

def is_safe(row, col, num):
    global grid
    for l in range(9):
        if grid[row][l] == num or grid[l][col] == num:
            return False;
    st_row = row - (row%3)
    st_col = col - (col%3)
    for m in range(3):
        for n in range(3):
            if grid[st_row+m][st_col+n] == num:
                return False
    return True

def is_safe_vict(row, col, num):
    global grid
    for l in range(9):
        if l!= col and grid[row][l] == num:
            return False
        if l != row and grid[l][col] == num:
            return False
    st_row = row - (row%3)
    st_col = col - (col%3)
    for m in range(3):
        for n in range(3):
            if(m != row and n != col):
                if grid[st_row+m][st_col+n] == num:
                    return False
    return True

def solve_sudoku(N, t):
    difference = datetime.now() - t
    seconds_in_day = 24 * 60 * 60
    timedelta(0, 8, 562000)
    total_secs = divmod(difference.days * seconds_in_day + difference.seconds, 60)[1]
    if(total_secs > 1):
        return False
    global grid
    i = 0
    j = 0
    f2 = False
    for i in random_x:
        flag = False
        for j in random_y:
            if grid[i][j]==0:
                flag = True
                f2 = True
                break
        if flag == True:
            break
    if f2 == False:
        return True
    for k in random_nos:
        if is_safe(i, j, k):
            grid[i][j] = k
            if solve_sudoku(N, t) == True:
                return True
            grid[i][j] = 0
    return False
    
def get_random_board():
    randomize()
    t1 = datetime.now()
    return solve_sudoku(9, t1)

def remove_items(num):
    global grid, allowed_cells
    for i in num:
        grid[i[0]][i[1]] = 0
        allowed_cells[i[0]][i[1]] = 1

def new_board(num):
    indexes = []
    for i in range(9):
        for j in range(9):
            indexes.append([i,j])
    choices = random.sample(indexes, num)
    while True:
        if get_random_board():
            break
    remove_items(choices)

def new_game():
    global CELLS_TO_DELETE
    new_board(CELLS_TO_DELETE)
    for i in range(10):
        color = "blue" if i % 3 == 0 else "gray"
        a = MARGIN + i * SIDE
        b = MARGIN
        c = MARGIN + i * SIDE
        d = HEIGHT - MARGIN
        my_canvas.create_line(a,b,c,d, fill=color)
        a = MARGIN
        b = MARGIN + i * SIDE
        c = WIDTH - MARGIN
        d = MARGIN + i * SIDE
        my_canvas.create_line(a,b,c,d, fill=color)
    set_up_board()
    
def submit():
    global sel_r, sel_c, vic_flag
    for i in range(9):
        f = False
        for j in range(9):
            if grid[i][j] == 0:
                #print(i,j, 'not filled')
                sel_r = i
                sel_c = j
                draw_bound()
                return False
            elif allowed_cells[i][j] == 1:
                if is_safe_vict(i,j,grid[i][j]) == False:
                    #print('wrong')
                    sel_r = i
                    sel_c = j
                    draw_bound()
                    return False
    #print('victory')
    victory()
    vic_flag = True
    return True

def victory():
    x0 = y0 = MARGIN + SIDE * 2
    x1 = y1 = MARGIN + SIDE * 7
    my_canvas.create_oval(x0, y0, x1, y1,tags="victory", fill="dark green", outline="green")
    x = y = MARGIN + 4 * SIDE + SIDE / 2
    my_canvas.create_text(x, y,text="You win!", tags="winner",fill="white", font=("Arial", 32))
    vic_flag = True
    
def set_up_board():
    global allowed_cells, w_r, w_c, sel_r, sel_c, vic_flag
    if vic_flag == True:
        my_canvas.delete("victory")
        vic_flag = False
    my_canvas.delete("numbers")
    for i in range(9):
        for j in range(9):
            answer = grid[i][j]
            if answer != 0:
                x = MARGIN + j * SIDE + SIDE / 2
                y = MARGIN + i * SIDE + SIDE / 2
                if allowed_cells[i][j] == 1:
                    color = "blue"
                else:
                    color = 'black'
                my_canvas.create_text(x, y, text=answer, tags="numbers", fill=color)

def clear_board():
    global allowed_cells, vic_flag
    if vic_flag == True:
        my_canvas.delete("victory")
        vic_flag = False
    my_canvas.delete("numbers")
    for i in range(9):
        for j in range(9):
            answer = grid[i][j]
            if allowed_cells[i][j] == 0:
                x = MARGIN + j * SIDE + SIDE / 2
                y = MARGIN + i * SIDE + SIDE / 2
                color = "black" 
                my_canvas.create_text(x, y, text=answer, tags="numbers", fill=color)
            else:
                grid[i][j] = 0

def change_diff(*args):
    global CELLS_TO_DELETE
    diff = variable.get()
    if diff == "Easy":
        CELLS_TO_DELETE = 20
    if diff == "Moderate":
        CELLS_TO_DELETE = 40
    if diff == "Difficult":
        CELLS_TO_DELETE = 60

    
def pressed(event):
    global sel_r, sel_c
    if sel_r >= 0 and sel_c >= 0 and event.char in "1234567890":
        grid[sel_r][sel_c] = int(event.char)
        sel_c, sel_r = -1, -1
        set_up_board()
        draw_bound()
                
def draw_bound():
    global sel_r, sel_c
    my_canvas.delete("cursor")
    if sel_r >= 0 and sel_c >= 0:
        a = MARGIN + sel_c * SIDE + 1
        b = MARGIN + sel_r * SIDE + 1
        c = MARGIN + (sel_c + 1) * SIDE - 1
        d = MARGIN + (sel_r + 1) * SIDE - 1
        my_canvas.create_rectangle(a,b,c,d, outline="red", tags="cursor")
            
def clicked(event):
    global sel_r, sel_c, allowed_cells
    x, y = event.x, event.y
    if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
        my_canvas.focus_set()
        row, col = int((y - MARGIN) / SIDE), int((x - MARGIN) / SIDE)
        if (row, col) == (sel_r, sel_c):
            sel_r, sel_c = -1, -1
        elif allowed_cells[row][col] == 1:
            sel_r, sel_c = row, col
    draw_bound()

OptionList = [
"Moderate",
"Easy",
"Difficult"]
variable = StringVar(root)
variable.set(OptionList[0])
opt = OptionMenu(root, variable, *OptionList)
opt.pack(fill=BOTH, side=TOP, expand=True)
variable.trace("w", change_diff)
newgame_button = Button(root,text="New Game",command=new_game)
newgame_button.pack(fill=BOTH, side=LEFT, expand=True)
clear_button = Button(root,text="Clear All",command=clear_board)
clear_button.pack(fill=BOTH, side=LEFT, expand=True)
clear_button = Button(text="Submit",command=submit)
clear_button.pack(fill=BOTH, side=RIGHT, expand=True)
new_game()
my_canvas.bind("<Button-1>", clicked)
my_canvas.bind("<Key>", pressed)           
root.mainloop()
