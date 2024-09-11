# -*- coding: utf-8 -*-

from tkinter import *
import pathlib
import random

# function allows switching frames 
def display_frame(current_frame,frame):
    current_frame.forget()
    frame.tkraise()

# Callback function for exit+save button
def save_exit():
    save(SAVE_PATH)
    w.destroy()

# Function for writing savedata to file
def save(path):
    with open(path, "w") as save:
        save.write(PLAYERNAME+",")
        save.write(str(PLAYERLEVEL)+",")
        save.write(str(PLAYERINVENTORY))
        playerlevel_var.set(str(PLAYERLEVEL))

# Function for loading savedata
def load(path, current_frame, frame):
    global PLAYERNAME, PLAYERLEVEL, PLAYERINVENTORY
    if not path.exists():
        print("making file")
        savefile = open(path, "w")
        savefile.write("empty")
        savefile.close()
    with open(path, "r") as savefile:
        PLAYERNAME, PLAYERLEVEL, PLAYERINVENTORY = savefile.read().split(",")
        PLAYERLEVEL = int(PLAYERLEVEL)
        playername_var.set(PLAYERNAME)
        playerlevel_var.set(str(PLAYERLEVEL))
        print(PLAYERNAME)
        print(PLAYERLEVEL)
        print(PLAYERINVENTORY)
    setup_level()
    display_frame(current_frame, frame)

# Only called once when initially getting the player's name
def get_name(name, current_frame, frame):
    global PLAYERNAME, PLAYERLEVEL, PLAYERINVENTORY
    playername_var.set(name)
    PLAYERNAME = name
    PLAYERLEVEL = 3
    # inventory system not really implemented as of yet
    PLAYERINVENTORY = ["Bronze sword"]

    save(SAVE_PATH)
    setup_level()
    display_frame(current_frame, frame)

# Called every time the player presses one of the movement buttons
# Marks the tile the player stood on as X and moves the peasant symbol
# Also calls the function that generates the informative text that is displayed on different tiles
def move_character(direction):
    global player_location

    tile_status[player_location[0]][player_location[1]].set("X")

    # If player moves up
    if direction == 0:
        if player_location[0] > 0:
            player_location[0] = player_location[0] - 1
            gen_tile_desc()
    # If player moves left
    elif direction == 1:
        if player_location[1] > 0:
            player_location[1] = player_location[1] - 1
            gen_tile_desc()
    # If player moves down
    elif direction == 2:
        if player_location[0] < 4:
            player_location[0] = player_location[0] + 1
            gen_tile_desc()
    # If player moves right
    elif direction == 3:
        if player_location[1] < 4:
            player_location[1] = player_location[1] + 1
            gen_tile_desc()
    
    tile_status[player_location[0]][player_location[1]].set("♙")

# This function generates the description text that is associated with every tile content.
def gen_tile_desc():
    # if starting tile
    if tile_contents[player_location[0]][player_location[1]].get() == "START":
        tile_desc.set("This is the safe starting tile")
        enter_button.config(state=DISABLED)
        fight_button.config(state=DISABLED)
    # if exit tile
    elif tile_contents[player_location[0]][player_location[1]].get() == "EXIT":
        tile_desc.set("You can enter the next dungeon level here")
        enter_button.config(state=NORMAL)
        fight_button.config(state=DISABLED)
    # if monster dead
    elif tile_contents[player_location[0]][player_location[1]].get() == "DEAD":
        tile_desc.set("This monster has been dead since the middle ages")
        enter_button.config(state=DISABLED)
        fight_button.config(state=DISABLED)
    # if monster
    else:
        tile_desc.set("A level " + str(tile_contents[player_location[0]][player_location[1]].get()))
        enter_button.config(state=DISABLED)
        fight_button.config(state=NORMAL)

# This function is called every time the player enters a door to a new level
# All the tiles are reset and setup_level() is called
def next_level():
    global player_location
    level_val = LEVEL.get()
    LEVEL.set(str(int(level_val)+1))
    for row in range(5):
        for column in range(5):
            tile_status[row][column].set("?")
    player_location = [4,2]
    tile_status[4][2].set("♙")
    enter_button.config(state=DISABLED)
    tile_desc.set("This is the safe starting tile")
    setup_level()

# This function generates all the tile contents and places monsters about with different levels
def setup_level():
    # Generate a exit tile that is not the enter tile
    exit_tile = []
    while True:
        exit_tile = [random.randint(0,4), random.randint(0,4)]
        if exit_tile != [4,2]:
            break
    # Go through every tile and add something in it
    for row in range(5):
        for column in range(5):
            calc_monster_level()
            tile_contents[row][column].set(monster_level.get() + " " + random.choice(MONSTERS))
            #print(tile_contents[row][column].get())
    
    tile_contents[4][2].set("START")
    tile_contents[exit_tile[0]][exit_tile[1]].set("EXIT")

# Randomize monster levels
def calc_monster_level():
    # a VERY simple system for giving monsters different levels
    monster_level.set(str(random.randint(PLAYERLEVEL-2, PLAYERLEVEL+5)))

# Super simple combat system
def fight_monster():
    global PLAYERLEVEL
    tempstring = tile_contents[player_location[0]][player_location[1]].get()
    print(tempstring)
    
    monsterinfo = tempstring.split(" ")
    monsterlvl = monsterinfo[0]
    monsterlvl = int(monsterlvl)
    if PLAYERLEVEL > monsterlvl:
        # kill monster
        # maybe add some formula to go up a certain amount based on monster strength
        PLAYERLEVEL += 1
        tile_contents[player_location[0]][player_location[1]].set("DEAD")
        tile_desc.set("Nothing to see here anymore")
        playerlevel_var.set(str(PLAYERLEVEL))
        fight_button.config(state=DISABLED)
    else:
        tile_desc.set("You need to be one level higher than the monster to kill it")
    

# Make tkinter window object
w = Tk()
w.geometry("800x600")
w.resizable(False,False)
w.title("Game")

LEVEL = StringVar()
LEVEL.set("1")
tile_desc = StringVar()
tile_desc.set("Starting tile, this is safe")
monster_level = StringVar()
playerlevel_var = StringVar()
playername_var = StringVar()
playername_var.set("default")

MONSTERS = ["Rat", "Cave wolf", "Giant rat", "Rattomancer", "Dragon"]
MONSTER_LOOT = {"Rat" : ["Rat sword", "Rat hat", "Rat armor", "Rat pants"],
            "Cave wolf" : ["Wolf sword", "Wolf armor", "Wolf pants", "Wolf hat"],
            "Giant rat" : ["Massive rat sword", "Gigantic rat hat"],
            "Rattomancer" : ["Rat staff", "Rat robes"],
            "Dragon" : ["Dragon longsword", "Dragon med helm", "Dragon chestplate", "Dragon platelegs"]}

player_location = [4,2]
PLAYERNAME = "default"
PLAYERLEVEL = 1
PLAYERINVENTORY = ["EMPTY"]
SAVE_PATH = pathlib.Path(__file__).parent.absolute() / "gamesave.txt"
FONT = ("Italianate", 30)
BTN_FONT = ("Italianate", 15)
SMALL_FONT = ("Italianate", 12)
COLORS = {
    "dark blue" : "#160647",
    "grey beige" : "#8b8878",
    "red wine red": "#3d1414",
    "button color": "#a295ac",
    "light gray" : "#808080",
    "dark gray" : "#525252",
    }
intro_string = "You find yourself at an entrance to what looks like a dungeon. How did you get here? Who knows, all you know is that you have to go kill some monsters."

# Create game frames
main_screen = Frame(w)
ng_screen = Frame(w)
game_screen = Frame(w)

#CURRENT_SCREEN = main_screen
# Placing all the different frames on top of each other and then simply raising them above another is the way I've chosed to organize
# my different windows
main_screen.grid(row=0,column=0)
ng_screen.grid(row=0,column=0)
game_screen.grid(row=0,column=0)

# GAME SCREEN NEEDS ALOT OF GLOBALS
game_screen_canvas = Canvas(game_screen, height=600, width=800, bg=COLORS.get("light gray"))
game_screen_canvas.create_rectangle(0,0,150,600,fill=COLORS.get("dark gray"))
game_screen_canvas.create_rectangle(650,0,800,600,fill=COLORS.get("dark gray"))
game_screen_canvas.grid(row=0,column=0)

# FRAME FOR THE MAP
map_frame = Frame(game_screen_canvas)
map_frame.place(relx=0.5,rely=0.4,anchor=CENTER)

# MATRIXES FOR TILES AND THEIR STATUS
map_tiles = [[],[],[],[],[]]
tile_status = [[],[],[],[],[]]
tile_contents = [[],[],[],[],[]]

for row in range(5):
    for column in range(5):
        tile_status[row].append(StringVar())
        tile_status[row][column].set("?")
        tile_contents[row].append(StringVar())
        tile_contents[row][column].set("Nothing")
        map_tiles[row].append(Label(map_frame,bg=COLORS.get("light gray"), height=3, width=6,textvariable=tile_status[row][column], font=SMALL_FONT,borderwidth=5, relief=GROOVE))

save_button_frame = Frame(game_screen_canvas)
save_button_frame.config(background=COLORS.get("light gray"))
save_button_frame.place(relx=0.72,rely=0.9, anchor=CENTER)
clickable_buttons_frame = Frame(game_screen_canvas)
clickable_buttons_frame.config(background=COLORS.get("light gray"))
clickable_buttons_frame.place(relx=0.55,rely=0.872, anchor=CENTER)

save_button = Button(save_button_frame, bg=COLORS.get("dark gray"), font=SMALL_FONT, text="Save and exit", command=save_exit, padx=2)
enter_button = Button(clickable_buttons_frame, bg=COLORS.get("light gray"), font=SMALL_FONT, text="Enter", command=next_level, state=DISABLED, height=3)
fight_button = Button(clickable_buttons_frame, bg=COLORS.get("light gray"), font=SMALL_FONT, text="Fight!", command=fight_monster, state=DISABLED, height=3)

tile_status[4][2].set("♙")


def main():

    # Setup and show the main screen
    main_screen_canvas = Canvas(main_screen, height=600, width=800, bg=COLORS.get("light gray"))
    main_screen_canvas.create_rectangle(0,0,150,600,fill=COLORS.get("dark gray"))
    main_screen_canvas.create_rectangle(650,0,800,600,fill=COLORS.get("dark gray"))
    main_screen_canvas.pack(side=BOTTOM, expand=0, fill="both")
    load_game = Button(main_screen_canvas, text="Load game",font=BTN_FONT,foreground=COLORS.get("red wine red"), bd="6", padx=50, bg=COLORS.get("button color"),
                       command=lambda:load(SAVE_PATH, main_screen, game_screen))
    start_new = Button(main_screen_canvas, text="Start a new adventure", font=BTN_FONT, foreground=COLORS.get("red wine red"), bd="6", padx=20, bg=COLORS.get("button color"),
                       command=lambda:display_frame(main_screen, ng_screen))
    load_game.place(relx=0.5, rely=0.6, anchor=CENTER)
    start_new.place(relx=0.5, rely=0.7, anchor=CENTER)
    
    label = Label(main_screen_canvas,text="A VERY BASIC DUNGEON GAME v.0.1", font=FONT, bg=COLORS.get("light gray"),
                    relief=FLAT, wraplength=500, fg=COLORS.get("red wine red"))
    label.place(relx=0.5, rely=0.3, anchor=CENTER)

    # Setup new game frame and widgets
    ng_screen_canvas = Canvas(ng_screen, height=600, width=800, bg=COLORS.get("light gray"))
    ng_screen_canvas.create_rectangle(0,0,150,600,fill=COLORS.get("dark gray"))
    ng_screen_canvas.create_rectangle(650,0,800,600,fill=COLORS.get("dark gray"))
    ng_screen_canvas.pack(side=BOTTOM, expand=0, fill="both")
    introlabel = Label(ng_screen, text=intro_string, font=SMALL_FONT, bg=COLORS.get("light gray"),
                    relief=FLAT, wraplength=400)
    introlabel.place(relx=0.5, rely=0.3, anchor=CENTER)
    namelabel = Label(ng_screen, text="But, first... What is your name?", font=SMALL_FONT, bg=COLORS.get("light gray"),
                    relief=FLAT, wraplength=400)
    namelabel.place(relx=0.5, rely=0.4, anchor=CENTER)
    entry = Entry(ng_screen, font=SMALL_FONT, bd=5, bg="light gray")
    entry.place(relx=0.5, rely=0.5, anchor=CENTER)
    submit_button = Button(ng_screen, text="Yes this is really my name", font=BTN_FONT, foreground=COLORS.get("red wine red"), bd="6", padx=20, bg=COLORS.get("button color"),
                       command=lambda:get_name(entry.get(), ng_screen, game_screen))
    submit_button.place(relx=0.5, rely=0.6, anchor=CENTER)


    # Setup game frame and widgets
    # FORMAT MAP TILES IN A GRID
    for i in range(5):
        for j in range(5):
            map_tiles[i][j].grid(row=i, column=j)
    
    # INTERACTABLE BUTTONS
    arrows = ["↑", "←", "↓", "→"]
    movement_buttons = []
    movement_buttons_frame = Frame(game_screen_canvas)
    movement_buttons_frame.config(background=COLORS.get("light gray"))
    movement_buttons_frame.place(relx=0.25,rely=0.75)

    # CREATE THE BUTTONS
    movement_buttons.append(Button(movement_buttons_frame, bg=COLORS.get("light gray"), font=("consolas", 20), text=arrows[0], height=1, width=3, command=lambda:move_character(0)))
    movement_buttons.append(Button(movement_buttons_frame, bg=COLORS.get("light gray"), font=("consolas", 20), text=arrows[1], height=1, width=3, command=lambda:move_character(1)))
    movement_buttons.append(Button(movement_buttons_frame, bg=COLORS.get("light gray"), font=("consolas", 20), text=arrows[2], height=1, width=3, command=lambda:move_character(2)))
    movement_buttons.append(Button(movement_buttons_frame, bg=COLORS.get("light gray"), font=("consolas", 20), text=arrows[3], height=1, width=3, command=lambda:move_character(3)))

    movement_buttons[0].grid(row=0, column=1)
    movement_buttons[1].grid(row=1, column=0)
    movement_buttons[2].grid(row=1, column=1)
    movement_buttons[3].grid(row=1, column=2)
    save_button.grid(row=0, column=2)
    enter_button.grid(row=0, column=0)
    fight_button.grid(row=0, column=1)

    # LABELS
    info_frame = Frame(game_screen_canvas)
    info_frame.config(background=COLORS.get("light gray"))
    info_frame.place(relx=0.4,rely=0.06, anchor=CENTER)
    
    player_name_label = Label(info_frame, background=COLORS.get("light gray"), textvariable=playername_var, font=("Italianate", 20), foreground=COLORS.get("red wine red"))
    level_text_label = Label(info_frame, background=COLORS.get("light gray"), text="Depth:", font=SMALL_FONT)
    level_label = Label(info_frame, background=COLORS.get("light gray"), textvariable=LEVEL, font=SMALL_FONT)
    player_level_text_label = Label(info_frame, background=COLORS.get("light gray"), text="Level:", font=SMALL_FONT)
    player_level_label = Label(info_frame, background=COLORS.get("light gray"), textvariable=playerlevel_var, text="placeholder", font=SMALL_FONT)

    player_name_label.grid(row=0, column=0)
    player_level_text_label.grid(row=0, column=1)
    player_level_label.grid(row=0, column=2)
    level_text_label.grid(row=0, column=3)
    level_label.grid(row=0, column=4)

    # Tile information
    tile_info_frame = Frame(game_screen_canvas, background=COLORS.get("light gray"))
    tile_info_frame.place(relx=0.2, rely=0.7)

    tile_desc_label = Label(tile_info_frame, background=COLORS.get("light gray"), font=SMALL_FONT, textvariable=tile_desc)
    tile_desc_label.grid(row=0, column=0)

    main_screen.tkraise()
    
    w.mainloop()

if __name__ == "__main__":
    main()