def append(audio, sound):
    """ the_audio += audio, None==empty """
    if sound is None:
        return audio
    if audio is None:
        return sound
    return audio + sound


def join(sounds):
    """ join list of sounds to one audio """
    audio = None
    for sound in sounds:
        if sound is None:
            return None
        audio = append(audio, sound)
    return audio
