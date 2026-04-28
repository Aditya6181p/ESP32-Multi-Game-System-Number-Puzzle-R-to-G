from machine import Pin, I2C
import ssd1306
import random
import time

# --- 1. Hardware Configuration ---
# Initialize I2C for the OLED (Standard pins for ESP32)
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Initialize Buttons with internal Pull-up resistors
# Using the safe pins we verified
btn_up    = Pin(27, Pin.IN, Pin.PULL_UP)
btn_down  = Pin(14, Pin.IN, Pin.PULL_UP)
btn_left  = Pin(18, Pin.IN, Pin.PULL_UP)
btn_right = Pin(19, Pin.IN, Pin.PULL_UP)

# --- 2. Game Variables ---
# 0 represents the empty sliding space
board = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]
a=[[0,0,0],[0,0,0],[0,0,0]]
a[0][0]='R'
a[2][2]='G'
r=[0,0]

empty_r, empty_c = 2, 2  # Starting position of '0'
box_size = 20
offset_x = 34  # Centers the 60px grid on 128px screen
offset_y = 2

# --- 3. Game Functions ---

def draw_board():
    """Clears and redraws the puzzle on the OLED"""
    oled.fill(0)
    for i in range(3):
        for j in range(3):
            x = offset_x + (j * box_size)
            y = offset_y + (i * box_size)
            
            # Draw the box border
            oled.rect(x, y, box_size, box_size, 1)
            
            # Draw the number (if not the empty space)
            val = board[i][j]
            if val != 0:
                # Offset text to center inside the box
                oled.text(str(val), x + 7, y + 6)
    oled.show()

def draw_grid():
    """Clears and redraws the puzzle on the OLED"""
    oled.fill(0)
    for i in range(3):
        for j in range(3):
            x = offset_x + (j * box_size)
            y = offset_y + (i * box_size)
            
            # Draw the box border
            oled.rect(x, y, box_size, box_size, 1)
            
            # Draw the number (if not the empty space)
            val = a[i][j]
            if val != 0:
                # Offset text to center inside the box
                oled.text(str(val), x + 7, y + 6)
    oled.show()

def swap(r1, c1, r2, c2):
    """Swaps two positions and updates the empty space tracker"""
    global empty_r, empty_c
    board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]
    empty_r, empty_c = r2, c2

def swap1(r1, c1, r2, c2):
    """Swaps two positions and updates the empty space tracker"""
    global empty_ro, empty_co
    a[r1][c1], a[r2][c2] = a[r2][c2], a[r1][c1]
    empty_ro, empty_co = r2, c2
    r[0]=empty_ro
    r[1]=empty_co

def shuffle(moves=60):
    """Simulates random valid moves to ensure the puzzle is solvable"""
    for _ in range(moves):
        r, c = empty_r, empty_c
        possible = []
        if r > 0: possible.append((r-1, c)) # Up
        if r < 2: possible.append((r+1, c)) # Down
        if c > 0: possible.append((r, c-1)) # Left
        if c < 2: possible.append((r, c+1)) # Right
        
        tr, tc = random.choice(possible)
        swap(r, c, tr, tc)

def check_win():
    """Checks if the board matches the solved state"""
    win_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    if board == win_state:
        oled.fill(0)
        oled.text("SOLVED!", 40, 35)
        oled.show()
        return True
    return False

# --- 4. Main Execution ---
while True:
    oled.fill(0)
    oled.text("Hello!", 40, 10)
    oled.text("1.Number Puzzle", 5, 20)
    oled.text("2.R to G", 5, 30)
    oled.text("3.Exit", 5, 40)
    oled.text("4.Suspense", 5, 50)
    oled.show()
    
    if not btn_up.value():
        print("Game Starting... Shuffling board.")
        shuffle(50)
        draw_board()
        while True:
            moved = False
            # Button logic: value() returns 0 when pressed because of PULL_UP
            if not btn_up.value() and empty_r > 0:
                swap(empty_r, empty_c, empty_r - 1, empty_c)
                moved = True
            elif not btn_down.value() and empty_r < 2:
                swap(empty_r, empty_c, empty_r + 1, empty_c)
                moved = True
            elif not btn_left.value() and empty_c > 0:
                swap(empty_r, empty_c, empty_r, empty_c - 1)
                moved = True
            elif not btn_right.value() and empty_c < 2:
                swap(empty_r, empty_c, empty_r, empty_c + 1)
                moved = True

            if moved:
                draw_board()
                if check_win():
                    time.sleep(3)
                    break
                # Debounce/Input speed control
                time.sleep(0.1) 
            # Essential for preventing the CPU from locking up
            time.sleep(0.1)
    elif not btn_down.value():
        draw_grid()
        empty_ro=0;
        empty_co=0;
        time.sleep(1)
        while True:
            moved = False
            # Button logic: value() returns 0 when pressed because of PULL_UP
            if not btn_up.value() and empty_ro > 0:
                swap1(empty_ro, empty_co, empty_ro - 1, empty_co)
                moved = True
            elif not btn_down.value() and empty_ro < 2:
                swap1(empty_ro, empty_co, empty_ro + 1, empty_co)
                moved = True
            elif not btn_left.value() and empty_co > 0:
                swap1(empty_ro, empty_co, empty_ro, empty_co - 1)
                moved = True
            elif not btn_right.value() and empty_co < 2:
                swap1(empty_ro, empty_co, empty_ro, empty_co + 1)
                moved = True
            if moved:
                draw_grid()
                # Debounce/Input speed control
                time.sleep(0.2)
                if r[0]==2 and r[1]==2:
                    oled.fill(0)
                    oled.text("Completed!",20,30)
                    oled.show()
                    time.sleep(3)
                    break
            # Essential for preventing the CPU from locking up
            time.sleep(0.01)
    elif not btn_right.value():
        oled.fill(0)
        oled.text("See Ya!", 40, 10)
        oled.text("    O     O    ", 5, 35)
        oled.text("       |   ", 5, 43)
        oled.text("       _   ", 5, 48)
        oled.text("    |_____|   ", 5, 55)
        oled.show()
        break
    elif not btn_left.value():
        oled.fill(0)
        oled.text("***************", 5, 0)
        oled.text("*   O     O   *", 5, 10)
        oled.text("*             *", 5, 20)
        oled.text("*    _____    *", 5, 27)
        oled.text("*   |     |   *", 5, 35)
        oled.text("*   |_____|   *", 5, 45)
        oled.text("*             *", 5, 55)
        oled.text("***************", 5, 60)
        oled.show()
        time.sleep(10)


