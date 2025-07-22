from main import Game, WinException, clear_screen

game = Game()
running = True

while running:
    try:
        game.run_tick()
    except WinException as e:
        clear_screen()
        print(f"Congratulations, {e}")
        input("Press Enter to exit...")
        break 
SystemExit()