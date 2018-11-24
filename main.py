#!/usr/bin/python3.6
# -*-coding:Utf-8 -*

import pygame
from pygame.locals import *
from random import randrange

# Colors
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Infos
TITLE = "PoissonGame by Baptiste"
VERSION = "1.0"

WIDTH, HEIGHT = 1280, 720

pygame.init()

window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(TITLE)

# Fonts
carton60 = pygame.font.Font('font/Carton_Six.ttf', 60)

dimbo38 = pygame.font.Font('font/Dimbo Regular.ttf', 38)
dimbo42 = pygame.font.Font('font/Dimbo Regular.ttf', 42)
dimbo46 = pygame.font.Font('font/Dimbo Regular.ttf', 46)
dimbo52 = pygame.font.Font('font/Dimbo Regular.ttf', 52)
dimbo56 = pygame.font.Font('font/Dimbo Regular.ttf', 56)
dimbo60 = pygame.font.Font('font/Dimbo Regular.ttf', 60)
dimbo64 = pygame.font.Font('font/Dimbo Regular.ttf', 64)


class PoissonGame:
    def __init__(self):
        """ Classe principale du jeu """
        # Images
        self.bg = pygame.image.load('img720/bg.jpg').convert()
        self.logo = pygame.image.load('img720/logo.png').convert_alpha()

        # Menus
        self.start = dimbo52.render("Commencer", 1, WHITE)
        self.restart = dimbo52.render("Recommencer", 1, WHITE)
        self.quitter = dimbo52.render("Quitter", 1, WHITE)

        # Infos
        self.game_over = False
        self.essais = 0

        # Scores
        self.score = 0
        self.highscore = 0

        # Vitesse du requin
        self.start_speed = 50
        self.speed_up = 5

        # Initialisation du requin
        self.shark = Mechant(WIDTH + 1000, randrange(-20, HEIGHT - 160), self.start_speed)

        # Initialisation du gentil
        self.gentil = Gentil()

    def reset(self):
        self.score = 0
        self.shark.speed = self.start_speed
        self.shark.set_pos(WIDTH + 389, randrange(-20, HEIGHT - 160))
        self.gentil.set_pos(20, 400)


    def set_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score

    def display_menu(self, window):
        window.blit(self.logo, (640 - 290, 50))

        window.blit(self.start, (640 - self.start.get_rect().width / 2, 300))
        window.blit(self.quitter, (640 - self.quitter.get_rect().width / 2, 350))

    def display_restart(self, window):
        gameover = carton60.render('GAME OVER !', 1, WHITE)
        votrescore = dimbo52.render("Votre score : %s" % self.score, 1, WHITE)
        highscore = dimbo38.render('Highscore : %s' % self.highscore, 1, WHITE)
        recommencer = dimbo52.render("Recommencer", 1, WHITE)
        quitter = dimbo52.render("Quitter", 1, WHITE)

        window.blit(gameover, (640 - gameover.get_rect().width / 2, 50))
        window.blit(votrescore, (640 - votrescore.get_rect().width / 2, 150))
        window.blit(highscore, (640 - highscore.get_rect().width / 2, 200))

        window.blit(recommencer, (640 - recommencer.get_rect().width / 2, 330))
        window.blit(quitter, (640 - quitter.get_rect().width / 2, 380))

    def update(self):
        if self.shark.x < - 389:
            self.score += 1
            self.shark.speed += self.speed_up

            self.shark.set_pos(WIDTH + 389, randrange(-20, HEIGHT - 160))
        else:
            self.shark.x -= self.shark.speed

        self.shark.update()
        self.gentil.update()

        self.game_over = self._check_collide()

    def _check_collide(self):
        return self.shark.hitbox.colliderect(self.gentil.hitbox)

    def display(self, window):
        window.blit(self.bg, (0,0))
        window.blit(self.gentil.img, self.gentil.get_pos())
        window.blit(self.shark.img, self.shark.get_pos())


class Mechant:
    def __init__(self, x, y, speed):
        self.img = pygame.image.load('img720/requin.png').convert_alpha()

        self.x = x
        self.y = y

        self.hitbox = pygame.Rect(self.x + 154, self.y + 108, 266, 111)

        self.speed = speed

    def get_pos(self):
        return self.x, self.y

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        self.hitbox = pygame.Rect(self.x + 154, self.y + 108, 266, 111)

    def display(self, window):
        window.blit(self.img, (self.x, self.y))


class Gentil:
    def __init__(self):
        self.img = pygame.image.load('img720/gentil.png').convert_alpha()

        self.x = 20
        self.y = 400

        self.hitbox = pygame.Rect(self.x + 97, self.y + 56, 123, 74)

        self.speed = 20

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def move(self, direction):
        if direction == 'up' and self.y > -10:
            self.y -= self.speed
        if direction == 'down' and self.y < 720-187:
            self.y += self.speed
        if direction == 'left' and self.x > -30:
            self.x -= self.speed
        if direction == 'right' and self.x > 1280-170:
            self.x += self.speed

    def get_pos(self):
        return self.x, self.y

    def update(self):
        self.hitbox = pygame.Rect(self.x + 97, self.y + 56, 123, 74)


poissongame = PoissonGame()

continuer = 1
main_menu = 1
game_on = 0
restart = 0
pause = False
pygame.key.set_repeat(1, 1)


main_menu_buttons = {'commencer': pygame.Rect(540, 312, 200, 40),
                     'quitter': pygame.Rect(540, 362, 200, 40)}
restart_menu_buttons = {'recommencer': pygame.Rect(510, 342, 260, 40),
                        'quitter': pygame.Rect(560, 392, 160, 40)}

while continuer:
    pygame.time.Clock().tick(120)

    """ Gestion des évènements """
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer, main_menu, game_on, restart = 0, 0, 0, 0

        if event.type == MOUSEBUTTONUP and event.button == 1:
            if main_menu:
                for text, rect in main_menu_buttons.items():
                    if rect.collidepoint(event.pos):
                        if text == 'quitter':
                            continuer, main_menu, game_on, restart = 0, 0, 0, 0
                        if text == 'commencer':
                            main_menu = 0
                            game_on = 1
            elif restart:
                for text, rect in restart_menu_buttons.items():
                    if rect.collidepoint(event.pos):
                        if text == 'quitter':
                            continuer, main_menu, game_on, restart = 0, 0, 0, 0
                        if text == 'recommencer':
                            poissongame.reset()
                            game_on = 1
                            restart = 0

        tkey = pygame.key.get_pressed()

        if game_on:
            if tkey[K_UP]:
                poissongame.gentil.move('up')
            if tkey[K_DOWN]:
                poissongame.gentil.move('down')
            if tkey[K_LEFT]:
                poissongame.gentil.x -= poissongame.gentil.speed
            if tkey[K_RIGHT]:
                poissongame.gentil.x += poissongame.gentil.speed

    """ Affichage du l'écran adéquat """
    # Menu principal
    if main_menu:
        poissongame.display(window)
        poissongame.display_menu(window)

    # Jeu
    if game_on:
        poissongame.update()
        poissongame.display(window)

        if poissongame.game_over:
            poissongame.set_highscore()
            game_on = 0
            restart = 1

    # Menu recommencer
    if restart:
        poissongame.display(window)
        poissongame.display_restart(window)


    pygame.display.flip()
pygame.quit()