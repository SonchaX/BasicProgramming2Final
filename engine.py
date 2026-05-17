import pygame
import sys
import random
from settings import *
from player import Player
from objects import Rock
from parallax import ParallaxBg
from ui import UI


class Sounds:
    def __init__(self):
        self.hit_sound = pygame.mixer.Sound("audio/damage.mp3")
        self.bg_music = pygame.mixer.Sound("audio/music.mp3")
        self.bg_music.set_volume(0.2)
        self.hit_sound.set_volume(0.5)

    def play_music(self):
        self.bg_music.play(-1)

    def stop_music(self):
        self.bg_music.stop()

    def play_hit(self):
        self.hit_sound.play()


class Level:
    def __init__(self, player):
        self.player = player
        self.all_sprites = pygame.sprite.Group()
        self.rocks = pygame.sprite.Group()

    def setup(self, levelNum):
        self.all_sprites = pygame.sprite.Group()
        self.rocks = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        if levelNum == 1:
            rockCount = 7
        else:
            rockCount = 7 + (levelNum * 2)

        for i in range(rockCount):
            newRock = Rock()
            newRock.speed += levelNum
            self.all_sprites.add(newRock)
            self.rocks.add(newRock)

    def resetPlayer(self):
        self.player.hp = 3
        self.player.distance = 0
        self.player.invincible = False

    def moveRocks(self, moveDir, speed):
        for rock in self.rocks:
            rock.rect.x -= speed * moveDir

        # I used the lambda we studied in class to find rocks outside the screen boundaries.

        out_of_bounds = list(filter(lambda r: r.rect.right < 0 or r.rect.left > WIDTH, self.rocks))
        
        # With this code I sent the rocks outside the border to the top
        
        for rock in out_of_bounds:
            rock.rect.y = random.randint(-300, -50)
            rock.rect.x = random.randint(0, WIDTH - 140)


class Engine:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Escape From The Avalanche")
        self.clock = pygame.time.Clock()

        self.state = "MENU"
        self.current_level = 1

        self.audio = Sounds()
        self.ui = UI(self.screen)
        self.player = Player()
        self.level = Level(self.player)
        self.level.setup(self.current_level)

        self.menu_bg = ParallaxBg(1)
        self.background = None

        self.menuChoice = 0
        self.pauseChoice = 0

    def startGame(self):
        self.current_level = 1
        self.level.resetPlayer()
        self.level.setup(self.current_level)
        self.background = ParallaxBg(self.current_level)
        self.state = "PLAYING"
        self.audio.play_music()

    def nextLevel(self):
        self.current_level += 1
        self.level.resetPlayer()
        self.level.setup(self.current_level)
        self.background = ParallaxBg(self.current_level)
        self.state = "PLAYING"
        self.audio.play_music()

    def goMenu(self):
        self.audio.stop_music()
        self.menuChoice = 0
        self.state = "MENU"

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if self.state == "MENU":
                    if event.key == pygame.K_DOWN:
                        self.menuChoice += 1
                        if self.menuChoice > 3:
                            self.menuChoice = 0
                    elif event.key == pygame.K_UP:
                        self.menuChoice -= 1
                        if self.menuChoice < 0:
                            self.menuChoice = 3
                    elif event.key == pygame.K_RETURN:
                        if self.menuChoice == 0:
                            self.startGame()
                        elif self.menuChoice == 1:
                            self.state = "CONTROLS"
                        elif self.menuChoice == 2:
                            self.state = "ABOUT"
                        elif self.menuChoice == 3:
                            pygame.quit()
                            sys.exit()

                elif self.state == "PLAYING":
                    if event.key == pygame.K_ESCAPE:
                        self.state = "PAUSE"
                        self.pauseChoice = 0
                        self.audio.stop_music()

                elif self.state == "PAUSE":
                    if event.key == pygame.K_DOWN:
                        self.pauseChoice += 1
                        if self.pauseChoice > 2:
                            self.pauseChoice = 0
                    elif event.key == pygame.K_UP:
                        self.pauseChoice -= 1
                        if self.pauseChoice < 0:
                            self.pauseChoice = 2
                    elif event.key == pygame.K_RETURN:
                        if self.pauseChoice == 0:
                            self.state = "PLAYING"
                            self.audio.play_music()
                        elif self.pauseChoice == 1:
                            self.goMenu()
                        elif self.pauseChoice == 2:
                            pygame.quit()
                            sys.exit()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "PLAYING"
                        self.audio.play_music()

                elif self.state == "NEXT_LEVEL":
                    if event.key == pygame.K_RETURN:
                        self.nextLevel()

                elif self.state == "GAMEOVER" or self.state == "WIN":
                    if event.key == pygame.K_RETURN:
                        self.goMenu()

                elif self.state == "CONTROLS" or self.state == "ABOUT":
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        self.state = "MENU"

    def update(self):
        if self.state == "MENU" or self.state == "CONTROLS" or self.state == "ABOUT":
            self.menu_bg.update("PLAYING", 1)

        # In this code, I tried to make the background and character stop if the game is stopped.
        if self.state != "PLAYING":
            return

        self.player.update()
        self.level.rocks.update()

        if self.player.is_moving:
            self.background.update(self.state, self.player.move_dir)

            if self.player.move_dir == 1:
                self.player.distance += 2

            self.level.moveRocks(self.player.move_dir, self.player.speed)

        if not self.player.invincible:
            # Here I check if a rock hit the player.
            hitList = pygame.sprite.spritecollide(self.player, self.level.rocks, False)
            if hitList:
                self.audio.play_hit()
                self.player.hp -= 1
                self.player.invincible = True
                self.player.invincibility_timer = 120

                if self.player.hp <= 0:
                    self.state = "GAMEOVER"
                    self.audio.stop_music()

        if self.player.distance >= LEVEL_LENGTH:
            self.audio.stop_music()
            if self.current_level < 4:
                self.state = "NEXT_LEVEL"
            else:
                self.state = "WIN"

    def draw(self):
        if self.state == "PLAYING":
            self.background.draw(self.screen)
            self.level.all_sprites.draw(self.screen)
            self.ui.show_hud(self.player.hp, self.player.distance, self.current_level)

        elif self.state == "MENU":
            self.menu_bg.draw(self.screen)
            self.ui.show_menu(self.menuChoice)

        elif self.state == "PAUSE":
            self.background.draw(self.screen)
            self.level.all_sprites.draw(self.screen)
            self.ui.show_pause(self.pauseChoice)

        elif self.state == "CONTROLS":
            self.menu_bg.draw(self.screen)
            self.ui.show_controls()

        elif self.state == "ABOUT":
            self.menu_bg.draw(self.screen)
            self.ui.show_about()

        elif self.state == "NEXT_LEVEL":
            self.ui.show_next_level(self.current_level)

        elif self.state == "GAMEOVER":
            self.ui.show_gameover()

        elif self.state == "WIN":
            self.ui.show_win()

        pygame.display.flip()
