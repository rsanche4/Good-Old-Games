import tkinter as tk
from tkinter import messagebox
import sys
import random

class ReversiGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Reversi")

        size_option = sys.argv[1] # CLASSIC, LARGE, MASSIVE, INFINITE

        if size_option=="CLASSIC":
            self.board_size = 8
            self.tile_size = 100
        elif size_option=="LARGE":
            self.board_size = 12
            self.tile_size = 75
        elif size_option=="MASSIVE":
            self.board_size = 16
            self.tile_size = 55
        elif size_option=="INFINITE":
            self.board_size = 20
            self.tile_size = 45          

        # Game constants
        self.colors = {
            'empty': '#2e8b57',  # sea green
            'black': 'black',
            'white': 'white',
            'highlight': '#98fb98',  # pale green
            'flip_highlight': '#ffcc00'  # yellow for flip animation
        }
        
        # Game state
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 'black'
        self.valid_moves = []
        self.animation_in_progress = False
        
        # Initialize UI
        self.create_board()
        self.setup_initial_pieces()
        self.update_valid_moves()
        self.draw_board()
        
        # Score display
        self.score_label = tk.Label(master, text="Black: 2 - White: 2", font=('Arial', 14))
        self.score_label.pack()
        
        # Current player display
        self.player_label = tk.Label(master, text="Current Player: Black", font=('Arial', 14))
        self.player_label.pack()
    
    def create_board(self):
        """Create the game board canvas"""
        canvas_size = self.board_size * self.tile_size
        self.canvas = tk.Canvas(
            self.master, 
            width=canvas_size, 
            height=canvas_size, 
            bg=self.colors['empty']
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)
        
        # Draw grid lines
        for i in range(self.board_size + 1):
            # Vertical lines
            self.canvas.create_line(
                i * self.tile_size, 0,
                i * self.tile_size, canvas_size,
                fill="black"
            )
            # Horizontal lines
            self.canvas.create_line(
                0, i * self.tile_size,
                canvas_size, i * self.tile_size,
                fill="black"
            )
    
    def setup_initial_pieces(self):
        """Place the initial 4 pieces in the center"""
        mid1 = self.board_size // 2 - 1
        mid2 = self.board_size // 2
        
        # Initial pieces
        self.board[mid1][mid1] = 'white'
        self.board[mid1][mid2] = 'black'
        self.board[mid2][mid1] = 'black'
        self.board[mid2][mid2] = 'white'
    
    def draw_board(self, highlight_flips=None):
        """Draw all pieces and highlights on the board"""
        for row in range(self.board_size):
            for col in range(self.board_size):
                x1 = col * self.tile_size
                y1 = row * self.tile_size
                x2 = x1 + self.tile_size
                y2 = y1 + self.tile_size
                
                # Clear the tile
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=self.colors['empty'],
                    outline="black"
                )
                
                # Draw highlight for valid moves
                if (row, col) in self.valid_moves:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill=self.colors['highlight'],
                        outline="black"
                    )
                
                # Draw the piece if it exists
                if self.board[row][col]:
                    color = self.colors[self.board[row][col]]
                    # Add special highlight for flipping pieces
                    if highlight_flips and (row, col) in highlight_flips:
                        color = self.colors['flip_highlight']
                    self.canvas.create_oval(
                        x1 + 5, y1 + 5,
                        x2 - 5, y2 - 5,
                        fill=color
                    )
    
    def update_valid_moves(self):
        """Find all valid moves for the current player"""
        self.valid_moves = []
        opponent = 'white' if self.current_player == 'black' else 'black'
        
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] is not None:
                    continue  # Skip occupied squares
                
                # Check all 8 directions
                for dr, dc in [(-1,-1), (-1,0), (-1,1),
                              (0,-1),          (0,1),
                              (1,-1),  (1,0),  (1,1)]:
                    r, c = row + dr, col + dc
                    if (0 <= r < self.board_size and 0 <= c < self.board_size and 
                        self.board[r][c] == opponent):
                        # Continue in this direction
                        r += dr
                        c += dc
                        found = False
                        while 0 <= r < self.board_size and 0 <= c < self.board_size:
                            if self.board[r][c] == self.current_player:
                                found = True
                                break
                            elif self.board[r][c] is None:
                                break
                            r += dr
                            c += dc
                        
                        if found:
                            self.valid_moves.append((row, col))
                            break  # No need to check other directions
    
    def handle_click(self, event):
        """Handle player clicks on the board"""
        if self.animation_in_progress:
            return
            
        col = event.x // self.tile_size
        row = event.y // self.tile_size
        
        if (row, col) in self.valid_moves:
            self.make_move(row, col)

    def count_flips(self, row, col):
        """Count how many opponent pieces would be flipped by a move at (row,col).
        Returns the total number of flips."""
        if self.board[row][col] is not None:
            return 0  # Not a valid move
        
        opponent = 'white' if self.current_player == 'black' else 'black'
        total_flips = 0
        
        for dr, dc in [(-1,-1), (-1,0), (-1,1),
                    (0,-1),          (0,1),
                    (1,-1),  (1,0),  (1,1)]:
            r, c = row + dr, col + dc
            flips_in_dir = 0
            
            while 0 <= r < self.board_size and 0 <= c < self.board_size:
                if self.board[r][c] == opponent:
                    flips_in_dir += 1
                    r += dr
                    c += dc
                elif self.board[r][c] == self.current_player:
                    total_flips += flips_in_dir
                    break
                else:  # Empty space
                    break
                    
        return total_flips    

    def make_move(self, row, col):
        """Place a piece with smooth flip animation"""
        if self.animation_in_progress:
            return
            
        self.animation_in_progress = True
        opponent = 'white' if self.current_player == 'black' else 'black'
        
        # Place the new piece immediately
        self.board[row][col] = self.current_player
        self.draw_board()
        
        # Find all pieces to flip
        flip_coords = []
        for dr, dc in [(-1,-1), (-1,0), (-1,1),
                      (0,-1),          (0,1),
                      (1,-1),  (1,0),  (1,1)]:
            r, c = row + dr, col + dc
            to_flip = []
            
            while (0 <= r < self.board_size and 0 <= c < self.board_size and 
                   self.board[r][c] == opponent):
                to_flip.append((r, c))
                r += dr
                c += dc
            
            if (0 <= r < self.board_size and 0 <= c < self.board_size and 
                self.board[r][c] == self.current_player):
                flip_coords.extend(to_flip)
        
        # Animate the flips
        if flip_coords:
            self.animate_flips(flip_coords, row, col)
        else:
            self.finish_move(row, col)

    def animate_flips(self, flip_coords, row, col):
        """Animate the flipping of pieces"""
        # Highlight pieces that will flip
        self.draw_board(highlight_flips=flip_coords)
        self.master.update()
        
        # Flip pieces in stages
        steps = 5
        for step in range(1, steps + 1):
            self.master.after(50 * step, lambda s=step: self.do_flip_step(flip_coords, s, steps, row, col))
        
        # Finalize after animation completes
        self.master.after(50 * (steps + 1), lambda: self.finalize_move(flip_coords, row, col))

    def do_flip_step(self, flip_coords, step, total_steps, row, col):
        """Perform one step of the flip animation"""
        # Calculate intermediate color
        if self.current_player == 'black':
            start_color = self.colors['white']
            end_color = self.colors['black']
        else:
            start_color = self.colors['black']
            end_color = self.colors['white']
            
        # Blend colors based on animation progress
        ratio = step / total_steps
        r1, g1, b1 = self.master.winfo_rgb(start_color)
        r2, g2, b2 = self.master.winfo_rgb(end_color)
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        color = f'#{r//256:02x}{g//256:02x}{b//256:02x}'
        
        # Draw intermediate state
        for (r, c) in flip_coords:
            x1 = c * self.tile_size + 5
            y1 = r * self.tile_size + 5
            x2 = x1 + self.tile_size - 10
            y2 = y1 + self.tile_size - 10
            self.canvas.create_oval(x1, y1, x2, y2, fill=color)
        
        # Keep the new piece visible
        x1 = col * self.tile_size + 5
        y1 = row * self.tile_size + 5
        x2 = x1 + self.tile_size - 10
        y2 = y1 + self.tile_size - 10
        self.canvas.create_oval(x1, y1, x2, y2, fill=self.colors[self.current_player])

    def finalize_move(self, flip_coords, row, col):
        """Complete the move after animation finishes"""
        # Actually flip the pieces in the board state
        for (r, c) in flip_coords:
            self.board[r][c] = self.current_player
        
        # Finish the move
        self.finish_move(row, col)

    def finish_move(self, row, col):
        """Complete the move and handle AI turn"""
        opponent = 'white' if self.current_player == 'black' else 'black'
        self.current_player = opponent
        self.update_valid_moves()
        self.draw_board()
        self.update_scores()
        
        gameovercheck = False
        if not self.valid_moves:
            self.current_player = 'white' if self.current_player == 'black' else 'black'
            self.update_valid_moves()
            
            if not self.valid_moves:
                gameovercheck = True
                self.animation_in_progress = False
                self.game_over()
                return
            else:
                self.animation_in_progress = False
                messagebox.showinfo("No Valid Moves", 
                                  f"{opponent.capitalize()} has no valid moves. {self.current_player.capitalize()} plays again.")
                return
        
        # AI move
        if self.current_player == "white" and not gameovercheck:
            self.animation_in_progress = False
            current_best_move = 0
            current_best_flips = 0
            for moveindex in range(len(self.valid_moves)):
                temp = self.count_flips(self.valid_moves[moveindex][0], self.valid_moves[moveindex][1])
                if temp>current_best_flips:
                    current_best_flips = temp
                    current_best_move = moveindex
            
            aimove = (self.valid_moves[current_best_move][0], self.valid_moves[current_best_move][1])
            
            if aimove not in self.valid_moves:
                aimove = random.choice(self.valid_moves)
                print("AI Has chosen randomly. Beep Boop AI glitched?")
            
            # Schedule AI move after short delay
            self.master.after(500, lambda: self.make_move(aimove[0], aimove[1]))
        else:
            self.animation_in_progress = False
    
    def update_scores(self):
        """Update the score display"""
        black = sum(row.count('black') for row in self.board)
        white = sum(row.count('white') for row in self.board)
        
        self.score_label.config(text=f"Black: {black} - White: {white}")
        self.player_label.config(text=f"Current Player: {self.current_player.capitalize()}")
    
    def game_over(self):
        """Handle game over condition"""
        black = sum(row.count('black') for row in self.board)
        white = sum(row.count('white') for row in self.board)
        
        if black > white:
            winner = "Black wins!"
        elif white > black:
            winner = "White wins!"
        else:
            winner = "It's a tie!"
        
        messagebox.showinfo("Game Over", f"Game over! {winner}\nFinal score: Black {black} - White {white}")
        
        # Ask to play again
        if messagebox.askyesno("Play Again?", "Would you like to play again?"):
            self.reset_game()
        else:
            self.master.quit()
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 'black'
        self.animation_in_progress = False
        self.setup_initial_pieces()
        self.update_valid_moves()
        self.draw_board()
        self.update_scores()

if __name__ == "__main__":
    if len(sys.argv)<2:
        print("Usage: python reversi.py [MODE]\nMode Options: CLASSIC, LARGE, MASSIVE, INFINITE\nExample: python reversi.py CLASSIC")
        sys.exit()

    root = tk.Tk()
    root.resizable(width=False, height=False)
    game = ReversiGame(root)
    root.mainloop()