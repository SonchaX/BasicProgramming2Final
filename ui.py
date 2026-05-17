import pygame
from settings import *


class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 38, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 72, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 28)

    def draw_Text(self, text, x, y, color=WHITE, big=False):
        if big:
            surf = self.title_font.render(text, True, color)
        else:
            surf = self.font.render(text, True, color)
        rect = surf.get_rect(center=(x, y))
        self.screen.blit(surf, rect)

    def draw_Small_Text(self, text, x, y, color=WHITE):
        surf = self.small_font.render(text, True, color)
        rect = surf.get_rect(center=(x, y))
        self.screen.blit(surf, rect)

    def draw_Overlay(self, alpha):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(alpha)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

    def show_menu(self, selectedIndex):
        self.draw_Overlay(140)
        self.draw_Text("ESCAPE THE AVALANCHE", WIDTH // 2, HEIGHT // 4, WHITE, True)

        options = ["START", "CONTROLS", "ABOUT", "QUIT"]
        for i in range(len(options)):
            if i == selectedIndex:
                label = "> " + options[i] + " <"
                color = (255, 220, 50)
            else:
                label = options[i]
                color = WHITE
            self.draw_Text(label, WIDTH // 2, HEIGHT // 2 - 40 + i * 70, color)

        self.draw_Small_Text("UP / DOWN to navigate   ENTER to select", WIDTH // 2, HEIGHT - 60)

    def show_pause(self, selectedIndex):
        self.draw_Overlay(180)
        self.draw_Text("PAUSED", WIDTH // 2, HEIGHT // 3, WHITE, True)

        options = ["RESUME", "MENU", "QUIT"]
        for i in range(len(options)):
            if i == selectedIndex:
                label = "> " + options[i] + " <"
                color = (255, 220, 50)
            else:
                label = options[i]
                color = WHITE
            self.draw_Text(label, WIDTH // 2, HEIGHT // 2 + i * 70, color)

        self.draw_Small_Text("ESC to resume quickly", WIDTH // 2, HEIGHT - 60)

    def show_controls(self):
        self.draw_Overlay(160)
        self.draw_Text("CONTROLS", WIDTH // 2, HEIGHT // 4, WHITE, True)
        self.draw_Text("HOW CAN I PLAY THIS GAME:", WIDTH // 2, HEIGHT // 2 - 80)
        self.draw_Small_Text("LEFT / RIGHT arrow keys - move the player", WIDTH // 2, HEIGHT // 2 - 20)
        self.draw_Small_Text("ESC - pause the game", WIDTH // 2, HEIGHT // 2 + 30)
        self.draw_Small_Text("ENTER - confirm / select", WIDTH // 2, HEIGHT // 2 + 80)
        self.draw_Small_Text("Press ESC or ENTER to go back", WIDTH // 2, HEIGHT - 60)

    def show_about(self):
        self.draw_Overlay(160)
        self.draw_Text("ABOUT", WIDTH // 2, HEIGHT // 4, WHITE, True)
        self.draw_Small_Text("The main purpose of Avalanche Escape", WIDTH // 2, HEIGHT // 2 - 80)
        self.draw_Small_Text("Run as far as you can without getting hit by rocks.", WIDTH // 2, HEIGHT // 2 - 30)
        self.draw_Small_Text("There are 4 levels. Each one gets harder.", WIDTH // 2, HEIGHT // 2 + 20)
        self.draw_Small_Text("Reach the end of all 4 levels to win!", WIDTH // 2, HEIGHT // 2 + 70)
        self.draw_Small_Text("Press ESC or ENTER to go back", WIDTH // 2, HEIGHT - 60)

    def show_gameover(self):
        self.screen.fill(BG_COLOR)
        self.draw_Text("CRUSHED BY ROCKS!", WIDTH // 2, HEIGHT // 3, WHITE, True)
        self.draw_Text("PRESS ENTER TO GO BACK TO MENU", WIDTH // 2, HEIGHT // 2)

    def show_next_level(self, level):
        self.screen.fill(BG_COLOR)
        self.draw_Text(f"LEVEL {level} CLEARED!", WIDTH // 2, HEIGHT // 3, WHITE, True)
        self.draw_Text("PRESS ENTER FOR NEXT LEVEL", WIDTH // 2, HEIGHT // 2)

    def show_win(self):
        self.screen.fill(BG_COLOR)
        self.draw_Text("YOU ESCAPED! GAME BEATEN!", WIDTH // 2, HEIGHT // 3, WHITE, True)
        self.draw_Text("PRESS ENTER TO GO BACK TO MENU", WIDTH // 2, HEIGHT // 2)

    def show_hud(self, hp, distance, level):
        progressPercent = int((distance / LEVEL_LENGTH) * 100)
        surf = self.font.render(f"Level: {level}  HP: {hp}  Progress: %{progressPercent}", True, WHITE)
        self.screen.blit(surf, (20, 20))
        self.draw_Small_Text("ESC - pause", WIDTH - 100, 30)