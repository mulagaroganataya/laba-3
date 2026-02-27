import tkinter as tk
from dataclasses import dataclass
import random
from tkinter import messagebox


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


def render(canvas: tk.Canvas, snake: list[Point], food: Point | None) -> None:
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

    if food is not None:
        draw_cell(canvas, food, cell, ox, oy, fill="red")

    for i, p in enumerate(snake):
        draw_cell(canvas, p, cell, ox, oy, fill=("green" if i == 0 else "darkgreen"))


def spawn_food(snake: list[Point]) -> Point:
    empty = [Point(x, y) for x in range(GRID_W) for y in range(GRID_H) if Point(x, y) not in snake]
    return random.choice(empty)


def main() -> None:
    root = tk.Tk()
    root.title("Snake")
    root.geometry("600x520")

    top = tk.Frame(root)
    top.pack(fill="x")

    status_var = tk.StringVar(value="Готово. Играй стрелками.")
    tk.Label(top, textvariable=status_var, anchor="w").pack(side="left", padx=8, pady=6, fill="x", expand=True)

    score_var = tk.StringVar(value="Счёт: 0")
    tk.Label(top, textvariable=score_var, anchor="e").pack(side="right", padx=8)

    canvas = tk.Canvas(root, bg="white", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    snake = [Point(12, 10), Point(11, 10), Point(10, 10)]
    direction = Point(1, 0)
    pending: Point | None = None
    food = spawn_food(snake)
    running = True
    score = 0

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

    def game_over(reason: str) -> None:
        nonlocal running
        running = False
        status_var.set(f"Конец игры: {reason}")
        messagebox.showinfo("Конец игры", f"{reason}\nСчёт: {score}")

    def step():
        nonlocal snake, direction, pending, food, running, score
        if not running:
            return

        if pending is not None:
            direction = pending
            pending = None

        head = snake[0]
        new_head = Point(head.x + direction.x, head.y + direction.y)

        if not (0 <= new_head.x < GRID_W and 0 <= new_head.y < GRID_H):
            game_over("Стена")
            return

        if new_head in snake:
            game_over("Сам в себя")
            return

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            score_var.set(f"Счёт: {score}")
            status_var.set("Съел еду!")
            food = spawn_food(snake)
        else:
            snake.pop()

        render(canvas, snake, food)
        root.after(SPEED_MS, step)

    canvas.bind("<Configure>", lambda e: render(canvas, snake, food))
    root.after(SPEED_MS, step)

    root.mainloop()


if __name__ == "__main__":
    main()
