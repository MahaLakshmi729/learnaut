import tkinter as tk
import customtkinter
import random
import os

# Set the appearance mode and default color theme
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class TicTacToeApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title("TIC-TAC-TOE")

        # Calculate the centered position
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 1100
        window_height = 580
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Create the back arrow button
        self.back_button = customtkinter.CTkButton(self, text="⬅", command=self.go_to_main)
        self.back_button.place(x=10, rely=1.0, anchor=tk.SW)
        #self.back_button.place(x=10, y=self.winfo_height()-50)

        # Create a title label
        self.title_label = customtkinter.CTkLabel(self, text="Tic Tac Toe", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label.place(relx=0.5, rely=0.1, anchor="center")

        # Create the board
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

        # Create buttons for each cell
        self.buttons = []
        button_size = 100
        button_padding = 10
        board_width = 3 * (button_size + button_padding) - button_padding
        board_height = 3 * (button_size + button_padding) - button_padding
        board_x = (window_width - board_width) // 2
        board_y = (window_height - board_height) // 2
        for row in range(3):
            button_row = []
            for col in range(3):
                button = customtkinter.CTkButton(self, text=' ', command=lambda r=row, c=col: self.make_move(r, c), width=button_size, height=button_size)
                button.place(x=board_x + col * (button_size + button_padding), y=board_y + row * (button_size + button_padding))
                button_row.append(button)
            self.buttons.append(button_row)

        # Create a label to display the current player
        self.player_label = customtkinter.CTkLabel(self, text="Player: X", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.player_label.place(relx=0.5, rely=0.9, anchor="center")

        # Initialize the current player
        self.current_player = 'X'

    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.buttons[row][col].configure(text=self.current_player)
            self.check_winner()
            self.switch_player()
            if self.current_player == 'O':
                self.computer_move()

    def switch_player(self):
        if self.current_player == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'
        self.player_label.configure(text=f"Player: {self.current_player}")

    def check_winner(self):
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                self.display_winner(row[0])
                return

        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                self.display_winner(self.board[0][col])
                return

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            self.display_winner(self.board[0][0])
            return
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            self.display_winner(self.board[0][2])
            return

        # Check for a tie
        if all(self.board[row][col] != ' ' for row in range(3) for col in range(3)):
            self.display_winner('Tie')
            return

    def display_winner(self, winner):
        if winner == 'Tie':
            message = "It's a tie!"
        else:
            message = f"Player {winner} is the winner!"
        tk.messagebox.showinfo("Game Over", message)
        self.reset_board()

    def reset_board(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        for row in self.buttons:
            for button in row:
                button.configure(text=' ')
        self.current_player = 'X'
        self.player_label.configure(text="Player: X")

    def computer_move(self):
        # Find available empty cells
        available_cells = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == ' ':
                    available_cells.append((row, col))

        # Randomly choose a cell
        if available_cells:
            row, col = random.choice(available_cells)
            self.make_move(row, col)
            
    def go_to_main(self):
        # Code to navigate to main.py
        self.destroy()
        os.system("python main.py")


if __name__ == "__main__":
    app = TicTacToeApp()
    app.mainloop()
