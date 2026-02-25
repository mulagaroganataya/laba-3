import tkinter as tk


GRID_W, GRID_H = 25, 20


def draw_grid(canvas: tk.Canvas) -> None:
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

    # легкая сетка
    for x in range(GRID_W + 1):
        x1 = ox + x * cell
        canvas.create_line(x1, oy, x1, oy + field_h, fill="#ddd")
    for y in range(GRID_H + 1):
        y1 = oy + y * cell
        canvas.create_line(ox, y1, ox + field_w, y1, fill="#ddd")


def main() -> None:
    root = tk.Tk()
    root.title("Snake")
    root.geometry("600x480")

    canvas = tk.Canvas(root, bg="white", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    canvas.bind("<Configure>", lambda e: draw_grid(canvas))

    root.mainloop()


if __name__ == "__main__":
    main()
