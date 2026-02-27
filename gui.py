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


class SnakeGame:
    def __init__(self) -> None:
        # ui
        self.root: tk.Tk | None = None
        self.canvas: tk.Canvas | None = None
        self.status_var: tk.StringVar | None = None
        self.score_var: tk.StringVar | None = None

        # state
        self.snake: list[Point] = []
        self.food: Point | None = None
        self.direction: Point = Point(1, 0)
        self.pending: Point | None = None
        self.running: bool = False
        self.score: int = 0

        # config
        self.grid_w: int = GRID_W
        self.grid_h: int = GRID_H
        self.speed_ms: int = SPEED_MS

    def run(
        self,
        grid_w: int = GRID_W,
        grid_h: int = GRID_H,
        speed_ms: int = SPEED_MS,
        title: str = "Snake",
        geometry: str = "600x520",
    ) -> None:
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.speed_ms = speed_ms

        root = tk.Tk()
        root.title(title)
        root.geometry(geometry)
        self.root = root

        # menu
        menubar = tk.Menu(root)
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Игра", menu=game_menu)
        root.config(menu=menubar)

        top = tk.Frame(root)
        top.pack(fill="x")

        self.status_var = tk.StringVar(value="Готово. Игра → Новая игра.")
        tk.Label(top, textvariable=self.status_var, anchor="w").pack(
            side="left", padx=8, pady=6, fill="x", expand=True
        )

        self.score_var = tk.StringVar(value="Счёт: 0")
        tk.Label(top, textvariable=self.score_var, anchor="e").pack(side="right", padx=8)

        self.canvas = tk.Canvas(root, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # bindings
        root.bind("<Up>", lambda e: self.request_turn(0, -1))
        root.bind("<Down>", lambda e: self.request_turn(0, 1))
        root.bind("<Left>", lambda e: self.request_turn(-1, 0))
        root.bind("<Right>", lambda e: self.request_turn(1, 0))

        self.canvas.bind("<Configure>", lambda e: self.render())

        # menu commands
        game_menu.add_command(label="Новая игра", command=self.new_game)
        game_menu.add_separator()
        game_menu.add_command(label="Выход", command=root.destroy)

        root.after(self.speed_ms, self.step)
        root.mainloop()

    # ===== game logic =====

    def new_game(self) -> None:
        self.score = 0
        self._set_score(0)
        self._set_status("Игра началась! Стрелки — движение.")

        self.direction = Point(1, 0)
        self.pending = None
        self.snake = [Point(12, 10), Point(11, 10), Point(10, 10)]
        self.food = self.spawn_food()
        self.running = True
        self.render()

    def request_turn(self, dx: int, dy: int) -> None:
        if not self.running:
            return
        nd = Point(dx, dy)
        if nd.x == -self.direction.x and nd.y == -self.direction.y:
            return
        self.pending = nd

    def step(self) -> None:
        # расписание следующего шага делаем всегда
        if self.root is None:
            return

        if self.running:
            if self.pending is not None:
                self.direction = self.pending
                self.pending = None

            head = self.snake[0]
            new_head = Point(head.x + self.direction.x, head.y + self.direction.y)

            if not (0 <= new_head.x < self.grid_w and 0 <= new_head.y < self.grid_h):
                self.game_over("Стена")
            elif new_head in self.snake:
                self.game_over("Сам в себя")
            else:
                self.snake.insert(0, new_head)
                if self.food is not None and new_head == self.food:
                    self.score += 1
                    self._set_score(self.score)
                    self.food = self.spawn_food()
                else:
                    self.snake.pop()

                self.render()

        self.root.after(self.speed_ms, self.step)

    def game_over(self, reason: str) -> None:
        self.running = False
        self._set_status(f"Конец игры: {reason}. Игра → Новая игра.")
        messagebox.showinfo("Конец игры", f"{reason}\nСчёт: {self.score}")

    def spawn_food(self) -> Point:
        empty = [
            Point(x, y)
            for x in range(self.grid_w)
            for y in range(self.grid_h)
            if Point(x, y) not in self.snake
        ]
        return random.choice(empty)

    # ===== rendering =====

    def draw_cell(self, p: Point, cell: int, ox: int, oy: int, fill: str) -> None:
        if self.canvas is None:
            return
        x1 = ox + p.x * cell
        y1 = oy + p.y * cell
        x2 = x1 + cell
        y2 = y1 + cell
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="black")

    def render(self) -> None:
        if self.canvas is None:
            return

        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 2 or h <= 2:
            return

        cell = min(w // self.grid_w, h // self.grid_h)
        field_w = self.grid_w * cell
        field_h = self.grid_h * cell
        ox = (w - field_w) // 2
        oy = (h - field_h) // 2

        self.canvas.create_rectangle(ox, oy, ox + field_w, oy + field_h, outline="black")

        if self.food is not None:
            self.draw_cell(self.food, cell, ox, oy, fill="red")

        for i, p in enumerate(self.snake):
            self.draw_cell(p, cell, ox, oy, fill=("green" if i == 0 else "darkgreen"))

    # ===== ui helpers =====

    def _set_status(self, text: str) -> None:
        if self.status_var is not None:
            self.status_var.set(text)

    def _set_score(self, value: int) -> None:
        if self.score_var is not None:
            self.score_var.set(f"Счёт: {value}")
