import pydub.playback as playback


def play(sound):
    if sound is not None:
        playback.play(sound)
