import tkinter as tk
from dataclasses import dataclass


GRID_W, GRID_H = 25, 20


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
    canvas.bind("<Configure>", lambda e: render(canvas, snake))

    root.mainloop()


if __name__ == "__main__":
    main()
