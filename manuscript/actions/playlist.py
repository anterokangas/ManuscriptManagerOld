class Playlist:
    import manuscript.language.constants as mc
    from manuscript.actors.role import Role
    from manuscript.actors.sound import Sound
    from manuscript.actors.group import Group
    from manuscript.actors.wait import Wait
    from manuscript.actors.settings import Settings

    DEFINING_ACTIONS = {
        mc.ROLE: Role,
        mc.SOUND: Sound,
        mc.GROUP: Group,
        mc.WAIT: Wait,
        mc.SETTINGS: Settings,
    }

    defining_actions = []
