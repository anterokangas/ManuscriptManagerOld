import manuscript.tools.audio as audio


def append(the_audio, sound):
    """ the_audio += asound, None==empty """
    if sound is None:
        return the_audio
    if the_audio is None:
        return sound
    return the_audio + sound


def join(sounds):
    """ Join list of sounds to one audio """
    the_audio = None
    for sound in sounds:
        if sound is None:
            return None
        the_audio = append(the_audio, sound)
    return the_audio


def overlay(sounds):
    """ Overlay lst of sounds to one audio """
    if sounds is None or len(sounds) == 0:
        return None
    sounds.sort(reverse=True,
                key=lambda x: len(x) if x is not None else 0)
    the_audio = sounds[0]
    for sound in sounds[1:]:
        if sound is None:
            return None
        the_audio = the_audio.overlay(sound)
    return the_audio
