import pygame
import random
import sys
from pygame.locals import *

# Initialize pygame
pygame.init()

# Get the screen information
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h  # Use full screen dimensions

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 123, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
LIGHT_RED = (255, 182, 193)

# Difficulty levels
DIFFICULTY = {
    "EASY": {"min": 1, "max": 50, "attempts": 10, "color": LIGHT_GREEN},
    "MEDIUM": {"min": 1, "max": 100, "attempts": 15, "color": LIGHT_BLUE},
    "HARD": {"min": 1, "max": 200, "attempts": 25, "color": LIGHT_RED}
}

class NumberGuessingGame:
    def __init__(self):
        # Create full screen surface
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Number Guessing Game")
        
        # Scale fonts based on screen size
        font_scale = min(WIDTH, HEIGHT) / 1000  # Base scaling factor
        self.title_font = pygame.font.SysFont("Arial", int(50 * font_scale), bold=True)
        self.large_font = pygame.font.SysFont("Arial", int(36 * font_scale), bold=True)
        self.medium_font = pygame.font.SysFont("Arial", int(28 * font_scale))
        self.small_font = pygame.font.SysFont("Arial", int(24 * font_scale))
        
        self.state = "SELECT_DIFFICULTY"  # Game states: SELECT_DIFFICULTY, PLAYING, GAME_OVER
        self.difficulty = None
        self.game_paused = False
        self.menu_open = False
        self.reset_game()
        
    def reset_game(self):
        self.attempts = 0
        self.game_over = False
        self.win = False
        self.guess = ""
        
        if self.difficulty:
            diff = DIFFICULTY[self.difficulty]
            self.min_number = diff["min"]
            self.max_number = diff["max"]
            self.max_attempts = diff["attempts"]
            self.secret_number = random.randint(self.min_number, self.max_number)
            self.message = f"Guess a number between {self.min_number} and {self.max_number}"
        else:
            self.message = "Select a difficulty level"
            
        self.guess_history = []
        
    def select_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.state = "PLAYING"
        self.reset_game()
        
    def toggle_menu(self):
        self.menu_open = not self.menu_open
        
    def toggle_pause(self):
        self.game_paused = not self.game_paused
        
    def get_back_button_rect(self):
        # Scale the back button based on screen size
        btn_width = WIDTH * 0.1
        btn_height = HEIGHT * 0.05
        return pygame.Rect(WIDTH * 0.05, HEIGHT * 0.05, btn_width, btn_height)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            # Handle ESC key to exit fullscreen or quit
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
                
            if event.type == MOUSEBUTTONDOWN:
                # Check if back button was clicked (when in PLAYING or GAME_OVER state)
                if self.state in ["PLAYING", "GAME_OVER"]:
                    back_button_rect = self.get_back_button_rect()
                    if back_button_rect.collidepoint(event.pos):
                        self.state = "SELECT_DIFFICULTY"
                        self.difficulty = None
                        self.reset_game()
                
                # Check if hamburger button was clicked
                hamburger_rect = pygame.Rect(WIDTH - WIDTH * 0.06, HEIGHT * 0.02, WIDTH * 0.04, HEIGHT * 0.05)
                if hamburger_rect.collidepoint(event.pos):
                    self.toggle_menu()
                    
                # Handle menu button clicks if menu is open
                if self.menu_open:
                    # Resume button
                    resume_button = pygame.Rect(WIDTH - WIDTH * 0.17, HEIGHT * 0.07, WIDTH * 0.15, HEIGHT * 0.05)
                    if resume_button.collidepoint(event.pos):
                        self.game_paused = False
                        self.menu_open = False
                        
                    # Pause button
                    pause_button = pygame.Rect(WIDTH - WIDTH * 0.17, HEIGHT * 0.13, WIDTH * 0.15, HEIGHT * 0.05)
                    if pause_button.collidepoint(event.pos):
                        self.game_paused = True
                        self.menu_open = False
                        
                    # Quit button
                    quit_button = pygame.Rect(WIDTH - WIDTH * 0.17, HEIGHT * 0.19, WIDTH * 0.15, HEIGHT * 0.05)
                    if quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                
                if self.state == "SELECT_DIFFICULTY":
                    # Check if any difficulty button was clicked
                    for difficulty in ["EASY", "MEDIUM", "HARD"]:
                        button_rect = self.get_difficulty_button_rect(difficulty)
                        if button_rect.collidepoint(event.pos):
                            self.select_difficulty(difficulty)
                    
            if not self.game_paused and self.state == "PLAYING":
                if event.type == KEYDOWN:
                    if event.key == K_RETURN and self.guess:
                        try:
                            guess_num = int(self.guess)
                            self.check_guess(guess_num)
                            self.guess = ""
                        except ValueError:
                            self.message = "Please enter a valid number!"
                    elif event.key == K_BACKSPACE:
                        self.guess = self.guess[:-1]
                    elif event.key in range(K_0, K_9 + 1) and len(self.guess) < 3:
                        self.guess += chr(event.key)
                        
            elif self.state == "GAME_OVER":
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        # Reset with same difficulty
                        self.state = "PLAYING"
                        self.reset_game()
                    elif event.key == K_m:
                        # Return to difficulty selection
                        self.state = "SELECT_DIFFICULTY"
                        self.difficulty = None
                        self.reset_game()
                    
    def check_guess(self, guess):
        self.attempts += 1
        
        difference = abs(guess - self.secret_number)
        
        if guess == self.secret_number:
            self.win = True
            self.state = "GAME_OVER"
            self.message = f"Congratulations! You guessed the number in {self.attempts} attempts!"
        elif self.attempts >= self.max_attempts:
            self.state = "GAME_OVER"
            self.message = f"Game Over! The number was {self.secret_number}"
        else:
            # Determine how close the guess is
            if difference <= self.max_number * 0.05:  # Within 5% of range
                feedback = "Very hot! 🔥"
                color = RED
            elif difference <= self.max_number * 0.1:  # Within 10% of range
                feedback = "Hot! 🔥"
                color = YELLOW
            elif difference <= self.max_number * 0.2:  # Within 20% of range
                feedback = "Warm 😊"
                color = YELLOW
            elif difference <= self.max_number * 0.3:  # Within 30% of range
                feedback = "Cool ❄️"
                color = BLUE
            else:
                feedback = "Cold! ❄️❄️"
                color = BLUE
                
            hint = "Higher 👆" if guess < self.secret_number else "Lower 👇"
            self.message = f"{feedback} Try {hint}. Attempts: {self.attempts}/{self.max_attempts}"
            
            # Add to history
            self.guess_history.append((guess, color))
            
    def get_difficulty_button_rect(self, difficulty):
        # Scale buttons based on screen size
        button_width = WIDTH * 0.3  # Make buttons wider
        button_height = HEIGHT * 0.08
        center_x = WIDTH // 2
        
        # Create more vertical space between buttons
        if difficulty == "EASY":
            return pygame.Rect(center_x - button_width/2, HEIGHT * 0.15, button_width, button_height)
        elif difficulty == "MEDIUM":
            return pygame.Rect(center_x - button_width/2, HEIGHT * 0.32, button_width, button_height)
        elif difficulty == "HARD":
            return pygame.Rect(center_x - button_width/2, HEIGHT * 0.49, button_width, button_height)
        
    def draw_difficulty_selection(self):
        # Draw title
        title = self.title_font.render("Number Guessing Game", True, PURPLE)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT * 0.08))
        self.screen.blit(title, title_rect)
        
        # Draw subtitle
        subtitle = self.medium_font.render("Select Difficulty Level", True, BLACK)
        subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, HEIGHT * 0.12))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Draw difficulty buttons with plenty of space for details underneath
        for difficulty in ["EASY", "MEDIUM", "HARD"]:
            button_rect = self.get_difficulty_button_rect(difficulty)
            diff_data = DIFFICULTY[difficulty]
            
            # Draw button
            pygame.draw.rect(self.screen, diff_data["color"], button_rect, border_radius=15)
            pygame.draw.rect(self.screen, BLACK, button_rect, 2, border_radius=15)
            
            # Draw button text
            button_text = self.large_font.render(difficulty, True, BLACK)
            button_text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, button_text_rect)
            
            # Draw difficulty details - significantly below the button
            details_text = self.medium_font.render(
                f"Range: {diff_data['min']}-{diff_data['max']}, Attempts: {diff_data['attempts']}", 
                True, BLACK
            )
            details_rect = details_text.get_rect(center=(button_rect.centerx, button_rect.bottom + button_rect.height * 0.6))
            self.screen.blit(details_text, details_rect)
    
    def draw_back_button(self):
        back_button_rect = self.get_back_button_rect()
        pygame.draw.rect(self.screen, LIGHT_BLUE, back_button_rect, border_radius=5)
        pygame.draw.rect(self.screen, BLACK, back_button_rect, 2, border_radius=5)
        
        back_text = self.small_font.render("Back", True, BLACK)
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        self.screen.blit(back_text, back_text_rect)
            
    def draw_hamburger_menu(self):
        # Draw hamburger button
        hamburger_rect = pygame.Rect(WIDTH - WIDTH * 0.06, HEIGHT * 0.02, WIDTH * 0.04, HEIGHT * 0.05)
        pygame.draw.rect(self.screen, DARK_GRAY, hamburger_rect, border_radius=5)
        
        # Draw hamburger icon lines
        line_height = HEIGHT * 0.004
        for i in range(3):
            line_rect = pygame.Rect(
                WIDTH - WIDTH * 0.05, 
                HEIGHT * 0.028 + i * HEIGHT * 0.012, 
                WIDTH * 0.02, 
                line_height
            )
            pygame.draw.rect(self.screen, WHITE, line_rect)
            
        # Draw menu if open
        if self.menu_open:
            # Draw menu background
            menu_bg = pygame.Rect(WIDTH - WIDTH * 0.17, HEIGHT * 0.065, WIDTH * 0.16, HEIGHT * 0.17)
            pygame.draw.rect(self.screen, WHITE, menu_bg, border_radius=10)
            pygame.draw.rect(self.screen, BLACK, menu_bg, 2, border_radius=10)
            
            # Resume button
            resume_button = pygame.Rect(WIDTH - WIDTH * 0.16, HEIGHT * 0.07, WIDTH * 0.14, HEIGHT * 0.05)
            pygame.draw.rect(self.screen, LIGHT_GREEN, resume_button, border_radius=5)
            resume_text = self.small_font.render("Resume", True, BLACK)
            resume_text_rect = resume_text.get_rect(center=resume_button.center)
            self.screen.blit(resume_text, resume_text_rect)
            
            # Pause button
            pause_button = pygame.Rect(WIDTH - WIDTH * 0.16, HEIGHT * 0.13, WIDTH * 0.14, HEIGHT * 0.05)
            pygame.draw.rect(self.screen, LIGHT_BLUE, pause_button, border_radius=5)
            pause_text = self.small_font.render("Pause", True, BLACK)
            pause_text_rect = pause_text.get_rect(center=pause_button.center)
            self.screen.blit(pause_text, pause_text_rect)
            
            # Quit button
            quit_button = pygame.Rect(WIDTH - WIDTH * 0.16, HEIGHT * 0.19, WIDTH * 0.14, HEIGHT * 0.05)
            pygame.draw.rect(self.screen, LIGHT_RED, quit_button, border_radius=5)
            quit_text = self.small_font.render("Quit", True, BLACK)
            quit_text_rect = quit_text.get_rect(center=quit_button.center)
            self.screen.blit(quit_text, quit_text_rect)
        
    def draw_game(self):
        diff_color = DIFFICULTY[self.difficulty]["color"]
        
        # Draw back button
        self.draw_back_button()
        
        # Draw game title with difficulty
        title = self.title_font.render(f"Number Guessing Game - {self.difficulty}", True, PURPLE)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT * 0.05))
        self.screen.blit(title, title_rect)
        
        # Scale game area based on screen size
        game_area = pygame.Rect(
            WIDTH * 0.05, HEIGHT * 0.12,
            WIDTH * 0.9, HEIGHT * 0.85
        )
        
        # Draw game area
        pygame.draw.rect(self.screen, WHITE, game_area, border_radius=15)
        pygame.draw.rect(self.screen, DARK_GRAY, game_area, 3, border_radius=15)
        
        # Draw message
        message_surface = self.medium_font.render(self.message, True, BLUE)
        message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT * 0.15))
        self.screen.blit(message_surface, message_rect)

        # If game is paused, show pause overlay
        if self.game_paused:
            # Semi-transparent overlay
            pause_overlay = pygame.Surface((game_area.width, game_area.height), pygame.SRCALPHA)
            pause_overlay.fill((0, 0, 0, 128))  # Semi-transparent black
            self.screen.blit(pause_overlay, (game_area.x, game_area.y))
            
            # Pause message
            pause_text = self.large_font.render("GAME PAUSED", True, WHITE)
            pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(pause_text, pause_rect)
            
            # Instruction to resume
            resume_text = self.medium_font.render("Click menu to resume", True, WHITE)
            resume_rect = resume_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + HEIGHT * 0.05))
            self.screen.blit(resume_text, resume_rect)
        else:
            # Draw input box
            input_box = pygame.Rect(WIDTH // 2 - WIDTH * 0.1, HEIGHT * 0.2, WIDTH * 0.2, HEIGHT * 0.06)
            pygame.draw.rect(self.screen, GRAY, input_box, border_radius=10)
            pygame.draw.rect(self.screen, BLACK, input_box, 2, border_radius=10)
            
            # Draw current guess
            if self.state == "PLAYING":
                guess_surface = self.large_font.render(self.guess, True, BLACK)
                guess_rect = guess_surface.get_rect(center=input_box.center)
                self.screen.blit(guess_surface, guess_rect)
                
                # Draw instructions
                instructions = self.small_font.render("Press ENTER to submit your guess", True, DARK_GRAY)
                instructions_rect = instructions.get_rect(center=(WIDTH // 2, HEIGHT * 0.28))
                self.screen.blit(instructions, instructions_rect)
            else:  # GAME_OVER state
                # Game over message
                if self.win:
                    result_text = self.large_font.render("You Won!", True, GREEN)
                else:
                    result_text = self.large_font.render(f"Game Over! Number was {self.secret_number}", True, RED)
                result_rect = result_text.get_rect(center=(WIDTH // 2, HEIGHT * 0.2))
                self.screen.blit(result_text, result_rect)
                
                # Restart instructions
                restart_text = self.medium_font.render("Press R to play again", True, BLUE)
                restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT * 0.25))
                self.screen.blit(restart_text, restart_rect)
                
                # Menu instructions
                menu_text = self.medium_font.render("Press M for main menu", True, BLUE)
                menu_rect = menu_text.get_rect(center=(WIDTH // 2, HEIGHT * 0.3))
                self.screen.blit(menu_text, menu_rect)
                
            # Draw guess history
            history_title = self.medium_font.render("Guess History:", True, BLACK)
            history_title_rect = history_title.get_rect(topleft=(WIDTH * 0.1, HEIGHT * 0.35))
            self.screen.blit(history_title, history_title_rect)
            
            # Display previous guesses - scale for full screen
            for i, (guess, color) in enumerate(self.guess_history[-10:]):  # Show last 10 guesses
                y_pos = HEIGHT * 0.4 + i * HEIGHT * 0.04
                guess_text = self.small_font.render(f"Guess #{i+1}: {guess}", True, color)
                self.screen.blit(guess_text, (WIDTH * 0.1, y_pos))
                
            # Draw range reminder
            range_text = self.small_font.render(f"Range: {self.min_number} - {self.max_number}", True, DARK_GRAY)
            range_rect = range_text.get_rect(topleft=(WIDTH * 0.7, HEIGHT * 0.35))
            self.screen.blit(range_text, range_rect)
            
            # Draw attempts counter
            attempts_text = self.small_font.render(f"Attempts: {self.attempts}/{self.max_attempts}", True, DARK_GRAY)
            attempts_rect = attempts_text.get_rect(topleft=(WIDTH * 0.7, HEIGHT * 0.4))
            self.screen.blit(attempts_text, attempts_rect)
            
            # Draw colored difficulty indicator
            diff_indicator = pygame.Rect(WIDTH * 0.7, HEIGHT * 0.45, WIDTH * 0.2, HEIGHT * 0.05)
            pygame.draw.rect(self.screen, diff_color, diff_indicator, border_radius=5)
            diff_text = self.small_font.render(self.difficulty, True, BLACK)
            diff_text_rect = diff_text.get_rect(center=diff_indicator.center)
            self.screen.blit(diff_text, diff_text_rect)
        
    def draw(self):
        # Background with gradient
        for y in range(HEIGHT):
            color_value = int(180 + (y / HEIGHT) * 50)
            pygame.draw.rect(self.screen, (color_value, color_value, color_value), (0, y, WIDTH, 1))
        
        if self.state == "SELECT_DIFFICULTY":
            self.draw_difficulty_selection()
        else:  # PLAYING or GAME_OVER states
            self.draw_game()
        
        # Always draw hamburger menu on top
        self.draw_hamburger_menu()
            
        # Update display
        pygame.display.flip()
        
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            self.handle_events()
            self.draw()
            clock.tick(30)

if __name__ == "__main__":
    game = NumberGuessingGame()
    game.run()