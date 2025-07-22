from levels import Levels
from player import Player
import os
import copy

class WinException(Exception):
    """Raised when player finishes last level"""
    pass

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Game:
    """
    Game: 
        handles game logic, player\'s input and displays level state

    Raises:
        WinException: If level_index == MAX_LEVEL, indicating the player won the game

    Tiles description:

        p (str) : Player tile (your character)
        w (str) : Wall tile (blocks player's movement)
        a (str) : Air tile (empty space)
        s (str) : Spike tile (kills the player)
        f (str) : Finish tile (completes the level and increases level_index by 1)
        d (str) : Door tile (requires key to open)
        k (str) : Key tile (opens the door when player.keys > 0 otherwise acts like a wall)
        e (str) : Empty tile (used for visual spacing)
    """
    GAME_UI = {
        "p": "@",
        "w": "#",
        "a": ".",
        "s": "*",
        "f": "+",
        "k": "-",
        "d": "o",
        "e": " "
    }
    MAX_LEVEL = 5


    def __init__(self):
        self.level = None
        self.level_index = 0
        self.player = Player()
        self.load_level(self.level_index)
        print("="*40)
        print("Use W A S D to move around the map")
        print("Type 'h' for help or 'l' for tiles legend")
        print("Type 'exit' to finish program")
        input("Press Enter to begin...")
    
    def load_level(self, level_index):

        """
        Method which loads next level

        Args:
            level_index (int) : Index of level to load
        Exceptions:
            WinException: player finished last level
        """

        if level_index == self.MAX_LEVEL:
            raise WinException("You won!")
        self.player.keys = 0
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
        print(f"Keys: {self.player.keys}")
        print(f"h - help")
        print(f"l - legend")
        print(f"r - restart")

    def run_tick(self):
        clear_screen()
        self.show_info()
        self.display_grid()
        self.make_move()


    
    def make_move(self):

        def death():
            self.player.keys = 0
            self.load_level(self.level_index)

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
            elif next_t == "e":
                return "empty"

        inp = str(input("Enter command: ").strip())
        next_tile = self.player.position.copy()

        if inp not in ["w", "a", "s", "d", "h", "l", "r", "restart", "exit"]:
            print("Invalid input! Use <h> if you need help!")
            input("Press Enter to continue...")
            return

        if inp == "w":
            next_tile[1] -= 1
        if inp == "s":
            next_tile[1] += 1
        if inp == "a":
            next_tile[0] -= 1
        if inp == "d":
            next_tile[0] += 1
        

        if inp == "h":
            clear_screen()
            print(f"Movement:\n  <w>: up\n  <a>: right\n  <s>: down\n  <d>: left\n  <r>: reset level\n  <restart>: restarts the game from 0\n  <exit>: exits the program\n")
            input("Press Enter to continue...")
            return
        if inp == "l":
            clear_screen()
            print(f"Tiles:\n  <#>: wall\n  <@>: player\n  <.>: air\n  <*>: spike\n  <->: key\n  <o>: door\n  <+>: finish\n")
            input("Press Enter to continue...")
            return
        if inp == "r":
            self.load_level(self.level_index)
            return
        if inp == "restart":
            self.level_index = 0
            self.load_level(0)
            return
        if inp == "exit":
            clear_screen()
            print("Game closed...")
            raise SystemExit()

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
            self.player.keys += 1
            self.level[self.player.position[1]][self.player.position[0]] = "a"
            self.player.position = next_tile
            self.level[self.player.position[1]][self.player.position[0]] = "p"

        elif next_state == "door":
            if self.player.keys < 1:
                pass
            else:
                self.level[self.player.position[1]][self.player.position[0]] = "a"
                self.player.position = next_tile
                self.level[self.player.position[1]][self.player.position[0]] = "p"
                self.player.keys -= 1