'''
import pygame

class Sound:
    def clear(self):
        pygame.mixer.init()

    def bgm(self):
        pygame.mixer.stop()
        sound_effect = pygame.mixer.Sound('bgm.mp3')
        sound_effect.play()

    def turn_change(self):
        pygame.mixer.stop()
        sound_effect = pygame.mixer.Sound('turn.mp3')
        sound_effect.play()

    def game_over(self):
        pygame.mixer.stop()
        sound_effect = pygame.mixer.Sound('gameover.mp3')
        sound_effect.play()
'''
