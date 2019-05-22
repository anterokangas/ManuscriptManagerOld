from inspect import isfunction

import manuscript.tools.constants as mc

from manuscript.tools.format import partial_words
from manuscript.tools.format import hide_hints
from manuscript.tools.format import to_lines
from manuscript.tools.format import try_partials
from manuscript.tools.format import format_line
# noinspection PyProtectedMember
from manuscript.tools.format import _aligned_line
from manuscript.tools.format import format_text
from manuscript.tools.format import Book

import manuscript.tools.format as fmt


def test_partial_words():
    assert list(partial_words("Kekkonen")) == [
        "Kekkonen", ""
    ]
    assert list(partial_words("Ranta-Perkiö")) == [
        "Ranta-Perkiö", "", "Ranta-", "Perkiö"
    ]
    assert list(partial_words("suo#ma#lai#nen")) == [
        "suomalainen", "",
        "suomalai-", "nen",
        "suoma-", "lainen",
        "suo-", "malainen"
    ]
    assert list(partial_words("-sanonta")) == [
        "-sanonta", ""
    ]
    assert list(partial_words("-sa#non#ta")) == [
        "-sanonta", "",
        "-sanon-", "ta",
        "-sa-", "nonta"
    ]
    assert list(partial_words("Tasa-arvo-oikeus#istuin")) == [
        "Tasa-arvo-oikeusistuin", "",
        "Tasa-arvo-oikeus-", "istuin",
        "Tasa-arvo-", "oikeusistuin",
        "Tasa-", "arvo-oikeusistuin"
    ]
    assert list(partial_words("-asen#ne")) == [
        '-asenne', '', '-asen-', 'ne'
    ]
    assert list(partial_words("asen#ne-")) == [
        'asenne-', '', 'asenne-', '', 'asen-', 'ne-'
    ]
    assert list(partial_words("-asen#ne-")) == [
        '-asenne-', '', '-asenne-', '', '-asen-', 'ne-'
    ]


def test_hide_hints():
    orig = "Tasa-arvo-oikeus#istuin"
    assert hide_hints("Tasa-arvo-oikeus-istuin", orig) == \
        "Tasa-arvo-oikeusistuin"
    assert hide_hints("Tasa-arvo-oikeus#istuin", orig) == \
        "Tasa-arvo-oikeusistuin"
    assert hide_hints("Tasa-arvo-oi#keus#is#tuin", orig) == \
        "Tasa-arvo-oi#keu#is#tuin"


def test_to_lines():
    text = "Seitsemän veljeksen aikajänne on kymmenisen vuotta. " \
           "Romaanin ajankohdaksi on usein arvioitu 1830- ja " \
           "1840-lukuja eli Kiven (s. 1834) itsensä lapsuusvuosia. " \
           "Määrittelyn perusteena on muun muassa se, että " \
           "lapsuudessaan ihminen omaksuu ympäristönsä tapahtumat, " \
           "sanastot ja tarinat."
    assert list(to_lines(text)) == [
        'Seitsemän veljeksen aikajänne on',
        'kymmenisen vuotta. Romaanin ajankohdaksi',
        'on usein arvioitu 1830- ja 1840-lukuja',
        'eli Kiven (s. 1834) itsensä',
        'lapsuusvuosia. Määrittelyn perusteena on',
        'muun muassa se, että lapsuudessaan',
        'ihminen omaksuu ympäristönsä tapahtumat,',
        'sanastot ja tarinat.'
    ]

    text = "Seitsemän veljeksen aikajänne on kym#me#ni#sen vuotta. " \
           "Romaanin ajankohdaksi on usein arvioitu 1830- ja " \
           "1840-lukuja eli Kiven (s. 1834) itsensä lapsuusvuosia. " \
           "Määrittelyn perusteena on muun muassa se, että " \
           "lapsuudessaan ihminen omaksuu ympäristönsä tapahtumat, " \
           "sanastot ja tarinat. Seitsemästä veljeksestä on tehty " \
           "lukuisia näytelmä- ja myös elo#kuva#sovituksia. "
    assert list(to_lines(text)) == [
        'Seitsemän veljeksen aikajänne on kymme-',
        'nisen vuotta. Romaanin ajankohdaksi on',
        'usein arvioitu 1830- ja 1840-lukuja eli',
        'Kiven (s. 1834) itsensä lapsuusvuosia.',
        'Määrittelyn perusteena on muun muassa',
        'se, että lapsuudessaan ihminen omaksuu',
        'ympäristönsä tapahtumat, sanastot ja',
        'tarinat. Seitsemästä veljeksestä on',
        'tehty lukuisia näytelmä- ja myös elo-',
        'kuvasovituksia.'
    ]

    text = "Seitsemän veljeksen aikajänne on kym#me#ni#sen vuotta. " \
           "Romaanin ajan#kohdaksi on usein arvioitu 1830- ja " \
           "1840-lukuja eli Kiven (s. 1834) it#sensä lapsuusvuosia. " \
           "Mää#rittelyn pe#rus#teena on muun muassa se, että " \
           "lap#suudessaan ihminen omak#suu ym#päristönsä tapahtumat, " \
           "sa#nas#tot ja ta#rinat. Seitsemästä vel#jek#ses#tä on teh#ty " \
           "lukuisia näytelmä- ja myös elo#kuva#sovituksia. "
    assert list(to_lines(text, max_width=35)) == [
        'Seitsemän veljeksen aikajänne on',
        'kymmenisen vuotta. Romaanin ajan-',
        'kohdaksi on usein arvioitu 1830- ja',
        '1840-lukuja eli Kiven (s. 1834) it-',
        'sensä lapsuusvuosia. Määrittelyn',
        'perusteena on muun muassa se, että',
        'lapsuudessaan ihminen omaksuu ym-',
        'päristönsä tapahtumat, sanastot ja',
        'tarinat. Seitsemästä veljeksestä on',
        'tehty lukuisia näytelmä- ja myös',
        'elokuvasovituksia.']


def test_try_partials():
    # Case 1: line_ === "" and first parts fit
    word_ = "Pää-ääliö-öljy-yö-öykkäri-ilkiö-öky-yö"
    line_ = ""
    max_width = 15
    assert try_partials(line_, word_, max_width) == (
        'Pää-ääliö-öljy-', 'yö-öykkäri-ilkiö-öky-yö'
    )

    # Case 2: line _ != "" and first pasrts fit
    line_ = 10*"a"
    max_width = 15
    assert try_partials(line_, word_, max_width) == (
        'aaaaaaaaaa Pää-', 'ääliö-öljy-yö-öykkäri-ilkiö-öky-yö'
    )

    " Second example of case 2"
    max_width = 10
    assert try_partials(line_, word_, max_width) == (
        'aaaaaaaaaa', 'Pää-ääliö-öljy-yö-öykkäri-ilkiö-öky-yö'
    )

    # Case 3: line_ == "" and no part fits
    # should return "", word_
    line_ = ""
    word_ = 15*"b" + "-" + 15*"c"
    max_width = 10
    assert try_partials(line_, word_, max_width) == (
        "", 15*"b" + "-" + 15*"c"
    )

    # Case 4: line != "" and no part fits
    # should return line_, word_
    line_ = 5*"a"
    word_ = 15*"b" + "-" + 15*"c"
    max_width = 10
    assert try_partials(line_, word_, max_width) == (
        5*"a", 15*"b" + "-" + 15*"c"
    )


def test_format_line():
    # Default values
    assert format_line() == mc.PAGE_WIDTH*" "
    line_ = "This a test line."
    # line != ""
    assert format_line(line_) == (
        mc.LEFT_MARGIN*" "
        + line_
        + (mc.PAGE_WIDTH
           - mc.LEFT_MARGIN
           - len(line_)
           - mc.RIGHT_MARGIN)*" "
        + mc.RIGHT_MARGIN*" "
    )
    # page_width != default
    assert format_line(line_, page_width=30) == (
            mc.LEFT_MARGIN * " "
            + line_
            + (30
               - mc.LEFT_MARGIN
               - len(line_)
               - mc.RIGHT_MARGIN) * " "
            + mc.RIGHT_MARGIN * " "
    )
    assert format_line(line_, left_margin=7) == (
            7 * " "
            + line_
            + (mc.PAGE_WIDTH
               - 7
               - len(line_)
               - mc.RIGHT_MARGIN) * " "
            + mc.RIGHT_MARGIN * " "
    )
    # right_margin ! ""
    assert format_line(line_, right_margin=10) == (
        mc.LEFT_MARGIN*" "
        + line_
        + (mc.PAGE_WIDTH
           - mc.LEFT_MARGIN
           - len(line_)
           - 10)*" "
        + 10*" "
    )
    # align = CENTER
    assert format_line(line_, align=mc.CENTER) == "{}".format(
        mc.LEFT_MARGIN*" "
        + int((mc.PAGE_WIDTH
               - mc.LEFT_MARGIN
               - len(line_)
               - mc.RIGHT_MARGIN)/2)*" "
        + line_
        + int((mc.PAGE_WIDTH
               - mc.LEFT_MARGIN
               - len(line_)
               - mc.RIGHT_MARGIN)/2+1)*" "
        + mc.RIGHT_MARGIN*" "
    )
    # align = RIGHT
    assert format_line(line_, align=mc.RIGHT) == "{}".format(
        mc.LEFT_MARGIN*" "
        + (mc.PAGE_WIDTH
           - mc.LEFT_MARGIN
           - len(line_)
           - mc.RIGHT_MARGIN)*" "
        + line_
        + mc.RIGHT_MARGIN*" "
    )

    assert format_line(line_, underline="=") == (
        mc.LEFT_MARGIN*" "
        + line_
        + (mc.PAGE_WIDTH
           - mc.LEFT_MARGIN
           - len(line_)
           - mc.RIGHT_MARGIN)*" "
        + mc.RIGHT_MARGIN*" "
        + "\n"
        + mc.LEFT_MARGIN*" "
        + len(line_)*"="
        + (mc.PAGE_WIDTH
           - mc.LEFT_MARGIN
           - len(line_)
           - mc.RIGHT_MARGIN)*" "
        + mc.RIGHT_MARGIN*" "
    )

    assert format_line(line_, align=mc.CENTER, underline="=") == "{}".format(
        mc.LEFT_MARGIN*" "
        + int((mc.PAGE_WIDTH
               - mc.LEFT_MARGIN
               - len(line_)
               - mc.RIGHT_MARGIN)/2)*" "
        + line_
        + int((mc.PAGE_WIDTH
               - mc.LEFT_MARGIN
               - len(line_)
               - mc.RIGHT_MARGIN)/2+1)*" "
        + mc.RIGHT_MARGIN*" "
        + "\n"
        + mc.LEFT_MARGIN*" "
        + int((mc.PAGE_WIDTH
               - mc.LEFT_MARGIN
               - len(line_)
               - mc.RIGHT_MARGIN)/2)*" "
        + len(line_)*"="
        + int((mc.PAGE_WIDTH
               - mc.LEFT_MARGIN
               - len(line_)
               - mc.RIGHT_MARGIN)/2+0.5)*" "
        + mc.RIGHT_MARGIN*" "
    )
    # align = RIGHT
    assert format_line(line_, align=mc.RIGHT, underline="=") == "{}".format(
        mc.LEFT_MARGIN*" "
        + (mc.PAGE_WIDTH
           - mc.LEFT_MARGIN
           - len(line_)
           - mc.RIGHT_MARGIN)*" "
        + line_
        + mc.RIGHT_MARGIN*" "
        + "\n"
        + mc.LEFT_MARGIN*" "
        + (mc.PAGE_WIDTH
           - mc.LEFT_MARGIN
           - len(line_)
           - mc.RIGHT_MARGIN)*" "
        + len(line_)*"="
        + mc.RIGHT_MARGIN*" "
    )


def test___aligned_line():
    left_margin = mc.LEFT_MARGIN
    line_ = "Test Line"
    max_width = mc.MAX_WIDTH
    right_margin = mc.LEFT_MARGIN

    align_code = mc.ALIGN_CODES[mc.LEFT]
    assert _aligned_line(left_margin, line_, align_code, max_width, right_margin) == (
        left_margin*" "
        + line_
        + (max_width-len(line_))*" "
        + right_margin*" "
    )
    align_code = mc.ALIGN_CODES[mc.CENTER]
    assert _aligned_line(left_margin, line_, align_code, max_width, right_margin) == (
        left_margin*" "
        + int((max_width-len(line_))/2)*" "
        + line_
        + int((max_width - len(line_))/2+0.5) * " "
        + right_margin*" "
    )
    align_code = mc.ALIGN_CODES[mc.RIGHT]
    assert _aligned_line(left_margin, line_, align_code, max_width, right_margin) == (
        left_margin*" "
        + (max_width-len(line_))*" "
        + line_
        + right_margin*" "
    )


def test_format_text():
    # Final text
    text_ = "Marilyn (Juice Les#kinen). Sa#nat: " \
            "Mä taivalsin läpi tuulen ja tuis#kun " \
            "näh#däkseni sun puuteri#huiskun. " \
            "Mä silmäni suljin ja sinut näin ty#tös#sä naapurin."
    page_width = 45
    par_width = page_width - mc.LEFT_MARGIN - mc.RIGHT_MARGIN

    assert format_text(text_, page_width=page_width) == (
           "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"Marilyn (Juice Leskinen). Sanat: Mä":<{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"taivalsin läpi tuulen ja tuiskun":<{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"nähdäkseni sun puuterihuiskun. Mä":<{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"silmäni suljin ja sinut näin tytös-":<{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"sä naapurin.":<{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
    )
    assert format_text(text_, page_width=page_width, align=mc.CENTER) == (
           "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"Marilyn (Juice Leskinen). Sanat: Mä":^{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"taivalsin läpi tuulen ja tuiskun":^{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"nähdäkseni sun puuterihuiskun. Mä":^{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"silmäni suljin ja sinut näin tytös-":^{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"sä naapurin.":^{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
    )
    assert format_text(text_, page_width=page_width, align=mc.RIGHT) == (
           "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"Marilyn (Juice Leskinen). Sanat: Mä":>{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"taivalsin läpi tuulen ja tuiskun":>{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"nähdäkseni sun puuterihuiskun. Mä":>{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"silmäni suljin ja sinut näin tytös-":>{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"sä naapurin.":>{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
    )
    assert format_text(text_,
                       page_width=page_width,
                       align=mc.CENTER,
                       caps=True) == (
           "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"Marilyn (Juice Leskinen). Sanat: Mä":^{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"taivalsin läpi tuulen ja tuiskun":^{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"nähdäkseni sun puuterihuiskun. Mä":^{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"silmäni suljin ja sinut näin tytös-":^{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"sä naapurin.":^{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
    ).upper()
    assert format_text(text_,
                       page_width=page_width,
                       align=mc.CENTER,
                       caps=True,
                       underline="-") == (
           "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"Marilyn (Juice Leskinen). Sanat: Mä":^{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{len("Marilyn (Juice Leskinen). Sanat: Mä")*"-":^{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"taivalsin läpi tuulen ja tuiskun":^{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{len("taivalsin läpi tuulen ja tuiskun")*"-":^{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"nähdäkseni sun puuterihuiskun. Mä":^{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{len("nähdäkseni sun puuterihuiskun. Mä")*"-":^{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"silmäni suljin ja sinut näin tytös-":^{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{len("silmäni suljin ja sinut näin tytös-")*"-":^{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"sä naapurin.":^{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{len("sä naapurin.")*"-":^{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
    ).upper()
    assert format_text(text_,
                       page_width=page_width,
                       align=mc.RIGHT,
                       leading_newline=False) == (
           ""
           + mc.LEFT_MARGIN*" "
           + f'{"Marilyn (Juice Leskinen). Sanat: Mä":>{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"taivalsin läpi tuulen ja tuiskun":>{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"nähdäkseni sun puuterihuiskun. Mä":>{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"silmäni suljin ja sinut näin tytös-":>{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"sä naapurin.":>{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
    )
    assert format_text(text_,
                       page_width=page_width,
                       align=mc.RIGHT,
                       trailing_newline=True) == (
           "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"Marilyn (Juice Leskinen). Sanat: Mä":>{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"taivalsin läpi tuulen ja tuiskun":>{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"nähdäkseni sun puuterihuiskun. Mä":>{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"silmäni suljin ja sinut näin tytös-":>{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + mc.LEFT_MARGIN*" "
           + f'{"sä naapurin.":>{par_width}}'
           + mc.RIGHT_MARGIN*" "
           + "\n"
           + "\n"
    )


def test_book___init__():
    p = Book(roles=["franz", "josef"])
    assert "franz" in p.__dict__
    assert isfunction(p._role_template_function(["franz"]))
    assert "josef" in p.__dict__
    assert isfunction(p._role_template_function(["josef"]))


def test_book__role_template_function():
    p = Book()
    assert isfunction(p._role_template_function(["franz"]))


def test_paragraphs():
    # title
    p = Book(roles=["franz", "josef"])
    title_width = mc.PAGE_WIDTH - fmt.TITLE["left_margin"] - fmt.TITLE["right_margin"]
    p.title("Wienin Kevät")
    assert p.text == (
        "\n"
        + fmt.TITLE["left_margin"]*" "
        + f'{"Wienin Kevät".upper():^{title_width}}'
        + fmt.TITLE["right_margin"]*" "
        + "\n"
        + fmt.TITLE["left_margin"]*" "
        + f'{len("Wienin Kevät".upper())*"=":^{title_width}}'
        + fmt.TITLE["right_margin"]*" "
        + "\n"
    )

    # title_line
    p = Book(roles=["franz", "josef"])
    title_line_width = mc.PAGE_WIDTH - fmt.TITLE_LINE["left_margin"] - fmt.TITLE_LINE["right_margin"]
    p.title_line("Versio 1")
    assert p.text == (
        fmt.TITLE_LINE["left_margin"]*" "
        + f'{"Versio 1":^{title_line_width}}'
        + fmt.TITLE_LINE["right_margin"]*" "
        + "\n"
    )

    # header
    p = Book(roles=["franz", "josef"])
    header_width = mc.PAGE_WIDTH - fmt.HEADER["left_margin"] - fmt.HEADER["right_margin"]
    p.header("I KOHTAUS: Kahvilassa")
    assert p.text == (
        "\n"
        + fmt.HEADER["left_margin"]*" "
        + f'{"I KOHTAUS: Kahvilassa".upper():<{header_width}}'
        + fmt.HEADER["right_margin"]*" "
        + "\n"
    )

    # synopsis
    p = Book(roles=["franz", "josef"])
    synopsis_width = mc.PAGE_WIDTH - fmt.SYNOPSIS["left_margin"] - fmt.SYNOPSIS["right_margin"]
    p.synopsis("Musiikin ja tanssiaisten suuret ystävät, her#rat Franz ja Josef, istuvat kahvilassa.")
    assert p.text == (
        "\n"
        + fmt.SYNOPSIS["left_margin"]*" "
        + f'{"Musiikin ja tanssiaisten suuret ystävät, her-":<{synopsis_width}}'
        + fmt.SYNOPSIS["right_margin"]*" "
        + "\n"
        + fmt.SYNOPSIS["left_margin"]*" "
        + f'{"rat Franz ja Josef, istuvat kahvilassa.":<{synopsis_width}}'
        + fmt.SYNOPSIS["right_margin"]*" "
        + "\n"
    )

    # parenthesis
    p = Book(roles=["franz", "josef"])
    parenthesis_width = mc.PAGE_WIDTH - fmt.PARENTHESIS["left_margin"] - fmt.PARENTHESIS["right_margin"]
    p.parenthesis("Musiikin ja tanssiaisten suuret ystävät, her#rat Franz ja Josef, istuvat kahvilassa.")
    assert p.text == (
        "\n"
        + fmt.PARENTHESIS["left_margin"]*" "
        + f'{"Musiikin ja tanssiaisten suuret ystävät, herrat Franz ja":<{parenthesis_width}}'
        + fmt.PARENTHESIS["right_margin"]*" "
        + "\n"
        + fmt.PARENTHESIS["left_margin"]*" "
        + f'{"Josef, istuvat kahvilassa.":<{parenthesis_width}}'
        + fmt.PARENTHESIS["right_margin"]*" "
        + "\n"
    )

    # name
    p = Book(roles=["franz", "josef"])
    name_width = mc.PAGE_WIDTH - fmt.NAME["left_margin"] - fmt.NAME["right_margin"]
    p.name("Franz ")
    assert p.text == (
        "\n"
        + fmt.NAME["left_margin"]*" "
        + f'{"Franz".upper():<{name_width}}'
        + fmt.NAME["right_margin"]*" "
        + "\n"
    )

    # reply
    p = Book(roles=["franz", "josef"])
    reply_width = mc.PAGE_WIDTH - fmt.REPLY["left_margin"] - fmt.REPLY["right_margin"]
    p.reply("Tuohan kuulostaa kuin Johan Straussin, niiden kolmen kuuluisan "
            "säveltäjän isän, valssi-musiikilta.")
    assert p.text == (
        fmt.REPLY["left_margin"]*" "
        + f'{"Tuohan kuulostaa kuin Johan Straussin, niiden":<{reply_width}}'
        + fmt.REPLY["right_margin"]*" "
        + "\n"
        + fmt.REPLY["left_margin"]*" "
        + f'{"kolmen kuuluisan säveltäjän isän, valssi-":<{reply_width}}'
        + fmt.REPLY["right_margin"]*" "
        + "\n"
        + fmt.REPLY["left_margin"]*" "
        + f'{"musiikilta.":<{reply_width}}'
        + fmt.REPLY["right_margin"]*" "
        + "\n"
    )

    # franz (generated function) = NAME + REPLY
    p = Book(roles=["franz", "josef"])
    reply_width = mc.PAGE_WIDTH - fmt.REPLY["left_margin"] - fmt.REPLY["right_margin"]
    p.franz("Tuohan kuulostaa kuin Johan Straussin, niiden kolmen kuuluisan "
            "säveltäjän isän, valssi-musiikilta.")
    assert p.text == (
        "\n"
        + fmt.NAME["left_margin"] * " "
        + f'{"Franz".upper():<{name_width}}'
        + fmt.NAME["right_margin"] * " "
        + "\n"
        + fmt.REPLY["left_margin"]*" "
        + f'{"Tuohan kuulostaa kuin Johan Straussin, niiden":<{reply_width}}'
        + fmt.REPLY["right_margin"]*" "
        + "\n"
        + fmt.REPLY["left_margin"]*" "
        + f'{"kolmen kuuluisan säveltäjän isän, valssi-":<{reply_width}}'
        + fmt.REPLY["right_margin"]*" "
        + "\n"
        + fmt.REPLY["left_margin"]*" "
        + f'{"musiikilta.":<{reply_width}}'
        + fmt.REPLY["right_margin"]*" "
        + "\n"
    )

    # 2x franz (or other Role)
    p = Book(roles=["franz", "josef"])
    reply_width = mc.PAGE_WIDTH - fmt.REPLY["left_margin"] - fmt.REPLY["right_margin"]

    p.franz("Tuohan kuulostaa kuin Johan Straussin, niiden kolmen kuuluisan "
            "säveltäjän isän, valssi-musiikilta.")
    p.franz("Tai ainakin valssilta.")

    assert p.text == (
            "\n"
            + fmt.NAME["left_margin"] * " "
            + f'{"Franz".upper():<{name_width}}'
            + fmt.NAME["right_margin"] * " "
            + "\n"
            + fmt.REPLY["left_margin"] * " "
            + f'{"Tuohan kuulostaa kuin Johan Straussin, niiden":<{reply_width}}'
            + fmt.REPLY["right_margin"] * " "
            + "\n"
            + fmt.REPLY["left_margin"] * " "
            + f'{"kolmen kuuluisan säveltäjän isän, valssi-":<{reply_width}}'
            + fmt.REPLY["right_margin"] * " "
            + "\n"
            + fmt.REPLY["left_margin"] * " "
            + f'{"musiikilta.":<{reply_width}}'
            + fmt.REPLY["right_margin"] * " "
            + "\n"
            + "\n"
            + fmt.REPLY["left_margin"] * " "
            + f'{"Tai ainakin valssilta.":<{reply_width}}'
            + fmt.REPLY["right_margin"] * " "
            + "\n"
    )


if __name__ == "__main__":
    test_partial_words()
    test_hide_hints()
    test_to_lines()
    test_try_partials()
    test_format_line()
    test___aligned_line()
    test_format_text()
    test_book___init__()
    test_book__role_template_function()
    test_paragraphs()
