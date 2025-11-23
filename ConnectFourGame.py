"""
Connect Four — Enhanced Tkinter GUI

Features:
 - Modern graphics with shadows and polished discs
 - Optional sound effects (drop + win)
 - Hover indicator showing where the disc will drop
 - Scoreboard that tracks Red vs Yellow
 - Restart button
 - Save & Load game state to "connect4_save.json"
 - Clean UI layout and responsive design

Run:
    python ConnectFourGame.py
"""


import json
import os
import tkinter as tk
from tkinter import messagebox

try:
    import winsound
except:
    winsound = None

ROWS = 6
COLS = 7
EMPTY = 0
PLAYER1 = 1   # Red
PLAYER2 = 2   # Yellow

SAVE_FILENAME = "connect4_save.json"


class ConnectFourGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect Four — Enhanced")
        self.root.minsize(760, 720)

        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.turn = PLAYER1
        self.score = {PLAYER1: 0, PLAYER2: 0}
        self.allow_sound = True

        # Top frame (scoreboard, buttons)
        top_frame = tk.Frame(root)
        top_frame.pack(fill="x", padx=8, pady=(8, 0))

        # Scoreboard
        self.score_label = tk.Label(top_frame, text=self._score_text(), font=("Segoe UI", 12, "bold"))
        self.score_label.pack(side="left", padx=6)

        # Sound toggle
        sound_chk = tk.Checkbutton(top_frame, text="Sound", command=self._toggle_sound)
        sound_chk.pack(side="left", padx=6)

        # Buttons
        restart_btn = tk.Button(top_frame, text="Restart", command=self.restart_game)
        restart_btn.pack(side="right", padx=6)

        load_btn = tk.Button(top_frame, text="Load", command=self.load_game)
        load_btn.pack(side="right", padx=6)

        save_btn = tk.Button(top_frame, text="Save", command=self.save_game)
        save_btn.pack(side="right", padx=6)

        # Canvas
        self.canvas_width = 700
        self.canvas_height = 600
        self.cell_size = self.canvas_width // COLS
        self.margin = 10

        self.canvas = tk.Canvas(root, width=self.canvas_width + 2 * self.margin,
                                height=self.canvas_height + 2 * self.margin, bg="#1b4f72",
                                highlightthickness=0)
        self.canvas.pack(padx=8, pady=8)

        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.hover_col = None

        # Bottom status bar
        bottom_frame = tk.Frame(root)
        bottom_frame.pack(fill="x", padx=8, pady=(0, 8))

        self.status_label = tk.Label(bottom_frame, text=self._status_text(), font=("Segoe UI", 11))
        self.status_label.pack(side="left", padx=6)

        # Draw initial board
        self.draw_board()

    def _score_text(self):
        return f"Score — Red: {self.score[PLAYER1]}    Yellow: {self.score[PLAYER2]}"

    def _status_text(self):
        return "Turn: Red" if self.turn == PLAYER1 else "Turn: Yellow"

    def _toggle_sound(self):
        self.allow_sound = not self.allow_sound

    def play_sound_drop(self):
        if not self.allow_sound: return
        try:
            if winsound:
                winsound.Beep(900, 70)
            else:
                self.root.bell()
        except:
            pass

    def play_sound_win(self):
        if not self.allow_sound: return
        try:
            if winsound:
                winsound.Beep(1200, 180)
                winsound.Beep(900, 130)
            else:
                self.root.bell()
        except:
            pass

    def draw_board(self):
        self.canvas.delete("all")
        w = self.canvas_width
        h = self.canvas_height
        cs = self.cell_size

        # Background
        self.canvas.create_rectangle(self.margin, self.margin, self.margin + w, self.margin + h,
                                     outline="", fill="#0b3a57")

        # Draw slots
        for r in range(ROWS):
            for c in range(COLS):
                x = self.margin + c * cs
                y = self.margin + r * cs

                # Shadow
                self.canvas.create_oval(x + 8, y + 8, x + cs - 8, y + cs - 8,
                                        fill="#082933", outline="")

                # Rim
                self.canvas.create_oval(x + 6, y + 6, x + cs - 6, y + cs - 6,
                                        fill="#b3cfe0", outline="")

                piece = self.board[r][c]

                if piece == PLAYER1:
                    fill = "#e53935"  # Red
                elif piece == PLAYER2:
                    fill = "#fdd835"  # Yellow
                else:
                    fill = "#ffffff"  # Empty slot

                # Piece center
                self.canvas.create_oval(x + 12, y + 12, x + cs - 12, y + cs - 12,
                                        fill=fill, outline="#777")

        # Hover indicator
        if self.hover_col is not None:
            col = self.hover_col
            x = self.margin + col * cs
            piece = self.turn
            fill = "#ff7b7b" if piece == PLAYER1 else "#fff59a"

            self.canvas.create_oval(x + 12, self.margin + 6, x + cs - 12, self.margin + cs - 12,
                                    fill=fill, stipple="gray25", outline="#555")

    def on_mouse_move(self, event):
        col = (event.x - self.margin) // self.cell_size
        if col < 0 or col >= COLS:
            self.hover_col = None
        else:
            self.hover_col = int(col)
        self.draw_board()

    def handle_click(self, event):
        col = (event.x - self.margin) // self.cell_size
        if col < 0 or col >= COLS:
            return

        row = self.get_available_row(col)
        if row is None:
            return

        self.board[row][col] = self.turn
        self.play_sound_drop()
        self.draw_board()

        if self.check_win(self.turn):
            winner = "Red" if self.turn == PLAYER1 else "Yellow"
            self.play_sound_win()
            messagebox.showinfo("Winner!", f"{winner} wins!")

            self.score[self.turn] += 1
            self.score_label.config(text=self._score_text())

            if messagebox.askyesno("Play Again?", "Restart game?"):
                self.restart_game()
            else:
                self.disable_board()
            return

        if self.is_board_full():
            messagebox.showinfo("Draw!", "The board is full — it's a draw!")
            if messagebox.askyesno("Play Again?", "Restart game?"):
                self.restart_game()
            else:
                self.disable_board()
            return

        self.turn = PLAYER1 if self.turn == PLAYER2 else PLAYER2
        self.status_label.config(text=self._status_text())
        self.draw_board()

    def get_available_row(self, col):
        for r in range(ROWS - 1, -1, -1):
            if self.board[r][col] == EMPTY:
                return r
        return None

    def check_win(self, piece):
        # Horizontal
        for r in range(ROWS):
            for c in range(COLS - 3):
                if all(self.board[r][c + i] == piece for i in range(4)):
                    return True

        # Vertical
        for r in range(ROWS - 3):
            for c in range(COLS):
                if all(self.board[r + i][c] == piece for i in range(4)):
                    return True

        # Diagonal /
        for r in range(ROWS - 3):
            for c in range(3, COLS):
                if all(self.board[r + i][c - i] == piece for i in range(4)):
                    return True

        # Diagonal \
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(self.board[r + i][c + i] == piece for i in range(4)):
                    return True

        return False

    def is_board_full(self):
        return all(self.board[0][c] != EMPTY for c in range(COLS))

    def restart_game(self):
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.turn = PLAYER1
        self.status_label.config(text=self._status_text())
        self.enable_board()
        self.draw_board()

    def disable_board(self):
        self.canvas.unbind("<Button-1>")

    def enable_board(self):
        self.canvas.bind("<Button-1>", self.handle_click)

    def save_game(self):
        data = {
            "board": self.board,
            "turn": self.turn,
            "score": self.score
        }
        with open(SAVE_FILENAME, "w") as f:
            json.dump(data, f)
        messagebox.showinfo("Saved", "Game saved successfully!")

    def load_game(self):
        if not os.path.exists(SAVE_FILENAME):
            messagebox.showwarning("Error", "No save file found.")
            return

        with open(SAVE_FILENAME, "r") as f:
            data = json.load(f)

        self.board = data["board"]
        self.turn = data["turn"]
        self.score = data["score"]

        self.score_label.config(text=self._score_text())
        self.status_label.config(text=self._status_text())

        self.enable_board()
        self.draw_board()
        messagebox.showinfo("Loaded", "Game loaded successfully!")


# -------------------------------------------
# MAIN RUNNER (Required for window to open)
# -------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ConnectFourGUI(root)
    root.mainloop()
