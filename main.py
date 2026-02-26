import tkinter as tk
from dataclasses import dataclass


GRID_W, GRID_H = 25, 20
SPEED_MS = 150


@dataclass(frozen=True)
class Point:
    x: int
    y: int


def draw_cell(canvas: tk.Canvas, p: Point, cell: int, ox: int, oy: int, fill: str) -> None:
    x1 = ox + p.x * cell
    y1 = oy + p.y * cell
    x2 = x1 + cell
    y2 = y1 + cell
    canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="black")


def render(canvas: tk.Canvas, snake: list[Point]) -> None:
    canvas.delete("all")
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    if w <= 2 or h <= 2:
        return

    cell = min(w // GRID_W, h // GRID_H)
    field_w = GRID_W * cell
    field_h = GRID_H * cell
    ox = (w - field_w) // 2
    oy = (h - field_h) // 2

    canvas.create_rectangle(ox, oy, ox + field_w, oy + field_h, outline="black")

    for i, p in enumerate(snake):
        draw_cell(canvas, p, cell, ox, oy, fill=("green" if i == 0 else "darkgreen"))


def main() -> None:
    root = tk.Tk()
    root.title("Snake")
    root.geometry("600x480")

    canvas = tk.Canvas(root, bg="white", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    snake = [Point(12, 10), Point(11, 10), Point(10, 10)]
    direction = Point(1, 0)
    pending: Point | None = None

    def request_turn(dx: int, dy: int) -> None:
        nonlocal pending, direction
        nd = Point(dx, dy)
        if nd.x == -direction.x and nd.y == -direction.y:
            return
        pending = nd

    root.bind("<Up>", lambda e: request_turn(0, -1))
    root.bind("<Down>", lambda e: request_turn(0, 1))
    root.bind("<Left>", lambda e: request_turn(-1, 0))
    root.bind("<Right>", lambda e: request_turn(1, 0))

    def step():
        nonlocal snake, direction, pending
        if pending is not None:
            direction = pending
            pending = None

        head = snake[0]
        new_head = Point(head.x + direction.x, head.y + direction.y)
        snake = [new_head] + snake[:-1]

        render(canvas, snake)
        root.after(SPEED_MS, step)

    canvas.bind("<Configure>", lambda e: render(canvas, snake))
    root.after(SPEED_MS, step)

    root.mainloop()


if __name__ == "__main__":
    main()
