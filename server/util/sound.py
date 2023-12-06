'''
import pygame

class Sound:
    def __init__(self):
        pygame.mixer.init()
        self.bgm_sound = pygame.mixer.Sound('bgm.mp3')
        self.turn_sound = pygame.mixer.Sound('turn.mp3')
        self.game_over_sound = pygame.mixer.Sound('gameover.mp3')

    def play_bgm(self):
        pygame.mixer.stop()
        self.bgm_sound.play()

    def play_turn_change(self):
        pygame.mixer.stop()
        self.turn_sound.play()

    def play_game_over(self):
        pygame.mixer.stop()
        self.game_over_sound.play()
'''
