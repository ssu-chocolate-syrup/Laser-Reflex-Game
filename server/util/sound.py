
from audioplayer import AudioPlayer
import os
class Sound:
    def __init__(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        project_root = os.path.abspath(os.path.join(script_dir, ".."))

        # Specify the path for each sound file
        bgm_path = os.path.join(project_root, "mp3", "bgm.mp3")
        turn_path = os.path.join(project_root, "mp3", "turn.mp3")
        game_over_path = os.path.join(project_root, "mp3", "gameover.mp3")

        self.bgm_sound = AudioPlayer(bgm_path)
        self.turn_sound = AudioPlayer(turn_path)
        self.game_over_sound = AudioPlayer(game_over_path)

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


