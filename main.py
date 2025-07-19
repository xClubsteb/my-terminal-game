from levels import Levels
from player import Player
import os
import copy

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Game:
    """
    Tiles description:

        p (str) : Player tile (your character)
        w (str) : Wall tile (blocks player's movement)
        a (str) : Air tile (empty space)
        s (str) : Spike tile (kills the player)
        f (str) : Finish tile (completes the level and increases level_index by 1)
    """
    GAME_UI = {
        "p": "@",
        "w": "#",
        "a": ".",
        "s": "*",
        "f": "+",
        "k": "-",
        "d": "o"
    }


    def __init__(self):
        self.level = None
        self.level_index = 0
        self.player = Player()
        self.load_level(self.level_index)
        self.display_grid()
    
    def load_level(self, level_index):
        self.player.has_key = False
        level_grid = copy.deepcopy(Levels[level_index]['grid'])
        level_start_pos = Levels[level_index]['start_pos']

        self.level = level_grid
        self.player.position = level_start_pos
        self.level[self.player.position[1]][self.player.position[0]] = "p"
    
    def display_grid(self):
        display = "\n"
        for row in self.level:
            display += "".join([self.GAME_UI[i] for i in row]) + "\n"
        print(display)

    def show_info(self):
        print(f"<- Level {self.level_index+1} ->")
        print(f"Key: {'Yes' if self.player.has_key else 'No'}")
        print(f"h - help")
        print(f"l - legend")

    def run_tick(self):
        clear_screen()
        self.show_info()
        self.display_grid()
        self.make_move()


    
    def make_move(self):

        def death():
            start_x, start_y = Levels[self.level_index]["start_pos"]
            cur_x, cur_y = self.player.position
            self.level[cur_y][cur_x] = 'a'
            self.level[start_y][start_x] = 'p'
            self.player.position = Levels[self.level_index]["start_pos"]

        def next_state_get(next_tile):
            x, y = next_tile
            next_t = self.level[y][x]
            if next_t == "w":
                return "wall"
            elif next_t == "a":
                return "air"
            elif next_t == "s":
                return "spike"
            elif next_t == "f":
                return "finish"
            elif next_t == "k":
                return "key"
            elif next_t == "d":
                return "door"

        inp = str(input("Input: ").strip())
        next_tile = self.player.position.copy()

        if inp == "w":
            next_tile[1] -= 1
        if inp == "s":
            next_tile[1] += 1
        if inp == "a":
            next_tile[0] -= 1
        if inp == "d":
            next_tile[0] += 1
        

        if inp == "h":
            print(f"Movement:\n  <w>: up\n  <a>: right\n  <s>: down\n  <d>: left\n  <r>: reset level\n  <restart>: restarts the game from 0\n  <exit>: exits the program\n")
            input("Press Enter to continue...")
        if inp == "l":
            print(f"Tiles:\n  <#>: wall\n  <@>: player\n  <.>: air\n  <*>: spike\n  <->: key\n  <o>: door\n  <+>: finish\n")
            input("Press Enter to continue...")
        if inp == "r":
            self.load_level(self.level_index)
            return
        if inp == "restart":
            self.level_index = 0
            self.load_level(0)
            return
        if inp == "exit":
            print("Game closed...")
            raise SystemExit()

        if inp == "debug":
            num = int(input("level: "))
            self.level_index = num - 1
            self.load_level(self.level_index)

        next_state = next_state_get(next_tile)

        if next_state == "air":
            self.level[self.player.position[1]][self.player.position[0]] = "a"
            self.player.position = next_tile
            self.level[self.player.position[1]][self.player.position[0]] = "p"
        elif next_state == "wall":
            pass
        elif next_state == "spike":
            death()
        elif next_state == "finish":
            self.level_index += 1
            self.load_level(self.level_index)
        elif next_state == "key":
            self.player.has_key = True
            self.level[self.player.position[1]][self.player.position[0]] = "a"
            self.player.position = next_tile
            self.level[self.player.position[1]][self.player.position[0]] = "p"
        elif next_state == "door":
            if not self.player.has_key:
                pass
            else:
                self.level[self.player.position[1]][self.player.position[0]] = "a"
                self.player.position = next_tile
                self.level[self.player.position[1]][self.player.position[0]] = "p"
                self.player.has_key = False

        
        


        
    
    

game = Game()

running = True
while running:
    game.run_tick()