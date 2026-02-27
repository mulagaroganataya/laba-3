from gui import (
    SnakeGame,
    GRID_W,
    GRID_H,
    SPEED_MS
)

def main() -> None:
    game = SnakeGame()
    game.run(grid_w=GRID_W, grid_h=GRID_H, speed_ms=SPEED_MS)


if __name__ == "__main__":
    main()
