import tkinter as tk


def main() -> None:
    root = tk.Tk()
    root.title("Snake")
    root.geometry("600x480")

    canvas = tk.Canvas(root, bg="white", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()
