'''
from audioplayer import AudioPlayer

class Sound:
    def __init__(self):
        self.bgm_sound = AudioPlayer("bgm.mp3")
        self.turn_sound = AudioPlayer("turn.mp3")
        self.game_over_sound = AudioPlayer("gameover.mp3")

    def play_bgm(self):
        self.bgm_sound.play(loop=True)

    def play_turn_change(self):
        self.turn_sound.play()

    def play_game_over(self):
        # 다른 모든 사운드 정지
        self.bgm_sound.stop()
        self.turn_sound.stop()

        # 게임 오버 사운드 재생
        self.game_over_sound.play()

'''
