from manuscript.tools.box_text import box_text


def test_box_text():
    text_lines = [
        "text",
        ]
    assert box_text(text_lines) == \
    "+------+\n| text |\n+------+"

    text_lines = [
        "text",
        "lines",
        ]
    assert box_text(text_lines) == \
           "+-------+\n| text  |\n| lines |\n+-------+"

    text_lines = [
        "text",
        "having long",
        "lines",
        ]
    assert box_text(text_lines) == \
        "+-------------+\n|    text     |\n| having long |\n|    lines    |\n+-------------+"

    text_lines = [
        "text",
        " having long ",
        "lines",
        ]
    assert box_text(text_lines) == \
        "+---------------+\n|     text      |\n|  having long  |\n|     lines     |\n+---------------+"

    # Also str input is ok

    text_lines = "text"
    assert box_text(text_lines) == \
    "+------+\n| text |\n+------+"

    text_lines = \
        """text
           having long
           lines"""
    assert box_text(text_lines) == \
        "+-------------+\n|    text     |\n| having long |\n|    lines    |\n+-------------+"
