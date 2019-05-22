class Playlist:
    import manuscript.tools.constants as mc
    from manuscript.actions.role import Role
    from manuscript.actions.sound import Sound
    from manuscript.actions.group import Group
    from manuscript.actions.wait import Wait
    from manuscript.actions.settings import Settings

    DEFINING_ACTIONS = {
        mc.ROLE: Role,
        mc.SOUND: Sound,
        mc.GROUP: Group,
        mc.WAIT: Wait,
        mc.SETTINGS: Settings,
    }

    defining_actions = []
