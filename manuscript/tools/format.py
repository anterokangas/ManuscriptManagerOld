from manuscript.tools.castings import list_
from manuscript.tools.box_text import page_text
from types import MethodType
import manuscript.tools.constants as mc

# Default text styles and their settings
TITLE = {
    "left_margin": 10,
    "right_margin": 10,
    "align": mc.CENTER,
    "caps": True,
    "underline": "=",
    "leading_newline": True,
}
TITLE_LINE = {
    "left_margin": 10,
    "right_margin": 10,
    "align": mc.CENTER,
    "caps": False,
    "leading_newline": False,
}
HEADER = {
    "left_margin": 5,
    "right_margin": 10,
    "align": mc.LEFT,
    "caps": True,
    "leading_newline": True,
}
SYNOPSIS = {
    "left_margin": 10,
    "right_margin": 10,
    "align": mc.LEFT,
    "leading_newline": True,
}
PARENTHESIS = {
    "left_margin": 5,
    "right_margin": 5,
    "align": mc.LEFT,
}
NAME = {
    "left_margin": 25,
    "right_margin": 5,
    "align": mc.LEFT,
    "caps": True,
    "leading_newline": True,
}
REPLY = {
    "left_margin": 15,
    "right_margin": 5,
    "align": mc.LEFT,
    "leading_newline": False,
}


def partial_words(word_orig, hyphen=mc.HYPHEN, hint=mc.HINT):
    """
    Split word_orig by hyphens and hints but not if hyphen is the first or last char

    Parameters
    ----------
    word_orig : str
        the word to be splitted
    hyphen :    char
        the char that marks the split points
    hint :      char
        hyphenation hint, also marks split points
    Returns
    -------
    yields list of pairs (part, rest), where
        part :  str
            the part up to hyphen (included)
        rest : str
    """
    word_ = word_orig.replace(hint, hyphen)
    parts = word_.split(hyphen)
    if parts[0] == "":
        parts.remove("")
    if word_[0] == hyphen:
        parts = [hyphen + parts[0]] + parts[1:]

    yield hide_hints(word_, word_orig)
    yield ""
    for i_part in range(len(parts)-1, 0, -1):

        first_part = hyphen.join(parts[:i_part]) + hyphen
        first_part = hide_hints(first_part, word_orig[:len(first_part)])
        yield first_part

        last_part = hyphen.join(parts[i_part:])
        last_part = hide_hints(last_part, word_orig[-len(last_part):])
        yield last_part


def hide_hints(part, orig, hint=mc.HINT):
    """ Hide char in part if corresponding char in orig is the hint char """
    len_part = len(part)
    for i in range(len_part-1, 0, -1):
        if orig[i-1:i] == hint:
            part = part[:i-1] + part[i:]
    return part


def to_lines(text_="", max_width=mc.MAX_WIDTH):
    """ Fit words in text to lines """
    words = list_(text_)
    line_ = ""
    for word_ in words:
        line_, rest = try_partials(line_, word_, max_width)
        while rest != "":
            if len(line_) + 1 + len(rest) >= max_width:
                yield line_
                line_, rest = try_partials("", rest, max_width)
                if line_ == "" and rest != "":
                    line_, rest = try_partials(rest[:max_width], rest[max_width:], max_width)
            else:
                line_, rest = try_partials(line_, rest, max_width)
    yield line_


def try_partials(line_, word_, max_width):
    """  Try to fit hyphenated (==partial) word to line_ """
    partials = partial_words(word_)
    rest = ""
    fit = False
    for part in partials:
        if line_ == "" and len(part) <= max_width:
            line_ = part
            rest = next(partials)
            fit = True
            break
        elif len(line_) + 1 + len(part) <= max_width:
            line_ = "".join([line_, " ", part])
            rest = next(partials)
            fit = True
            break
        rest = ""
        next(partials)
    if not fit:
        rest = word_
    return line_, rest


def format_line(
        line_="",
        page_width=mc.PAGE_WIDTH,
        left_margin=mc.LEFT_MARGIN,
        right_margin=mc.RIGHT_MARGIN,
        align=mc.ALIGN,
        min_width=mc.MIN_WIDTH,
        underline=""):
    """
    Convert line of text to a formatted form

    Parameters
    ----------
    line_ :         str
        The line to be formatted
    page_width :    int
        The width of final lines in page
    left_margin : int
        Number of spaces in the left
    right_margin : int
        Number of spaces in the right
    align : str in {mc.LEFT, mc.RIGHT, mc.CENTER
        Justification
    min_width : int
        Minimum width of the paragraph == page_width - left_margin - right_margin
    underline : str
        The characer that is used to underline text. "" == no underlining

    Returns
    -------
    str
        Formatted text line(s), all of length page_length and ending newline

    """
    max_width = page_width - left_margin - right_margin
    assert left_margin >= 0
    assert right_margin >= 0
    assert min_width >= mc.MIN_WIDTH
    assert max_width >= min_width
    align_code = mc.ALIGN_CODES.get(align, None)
    assert align_code is not None

    formatted_line = _aligned_line(left_margin, line_, align_code, max_width, right_margin)

    if underline != "":
        formatted_line += "\n" + _aligned_line(
            left_margin, len(line_)*underline, align_code, max_width, right_margin)

    return formatted_line


def _aligned_line(left_margin, line_, align_code, max_width, right_margin):
    """ Align a line
    
    Parameters
    ----------
    left_margin :   int
        Width of left margin
    line_  :        str
        The line to be aligned
    align_code :    str
        A valid aliign code, in {"<", "^", ">"}
    max_width :     int
        Width between marginals
    right_margin :  int
        Width of right margin

    Returns
    -------
    str 
        Formatted line
    """"""
    Align aline 
    
    """
    formatted_line = ""
    if left_margin > 0:
        formatted_line += f"{'':{left_margin}}"
    formatted_line += f"{line_:{align_code}{max_width}}"
    if right_margin > 0:
        formatted_line += f"{'':{right_margin}}"
    return formatted_line


def format_text(text_="",
                page_width=mc.PAGE_WIDTH,
                left_margin=mc.LEFT_MARGIN,
                right_margin=mc.RIGHT_MARGIN,
                align=mc.ALIGN,
                min_width=mc.MIN_WIDTH,
                caps=mc.CAPS,
                underline=mc.UNDERLINE,
                leading_newline=mc.LEADING_NEWLINE,
                trailing_newline=mc.TRAILING_NEWLINE):
    """
    Format long text string as one paragraph

    Change font case, split to lines, format lines and add leading and/or trailing newlines
    Parameters
    ----------
    text_ :         str
        the text to be formatted
    page_width :    int
        the width of each line, includeing marginals
    left_margin :   int
        number of spaces in left margin
    right_margin :  int
        number of spaces in right margin
    align : str in {mc.LEFT, mc.CENTER, mc.RIGHT}
        justification of each line
    min_width :     int
        minimum width of text between marginals
    caps :          bool
        is the case upper cas or not
    underline :     str
        ""     --> no underline
        a char --> the line is underlined using the char (if longer, first char s used)
    leading_newline :   bool
        is there an additional newline before all lines
    trailing_newline :  bool
        is there an additional newline after all lines

    Returns
    -------
    str
        formatted text following a newline
    """
    max_width = page_width - left_margin - right_margin
    if caps:
        text_ = text_.upper()
    formatted_text = "\n".join([format_line(line_,
                                            page_width=page_width,
                                            left_margin=left_margin,
                                            right_margin=right_margin,
                                            align=align,
                                            min_width=min_width,
                                            underline=underline)
                                for line_ in to_lines(
                                    text_, max_width)])

    if leading_newline:
        formatted_text = "\n" + formatted_text

    if trailing_newline:
        formatted_text = formatted_text + "\n"

    return formatted_text + "\n"


class Book:
    """
    Formats text

    Fit text to paragraphs containing formatted lines
    Standard styles and their default definitions' description
        title :         centered, capitalized, underlined, wide margins
        title_line :    centered, wide margins
        synopsis :      left justified, medium margins
        header :        left justified, capitalized, tiny margins
        parenthesis :   left justified, tiny margins
        name :          left justified, capaitalized, huge left margin
        reply :         left justified, medium margins
    Role styles :       combination of name followed by reply, but
                        if same role follows, the name is not repeated

    Result in attribute 'text'
    """
    def __init__(self, **kwargs):
        """
        Define paragraph styles

        The default styles can be overridden, otherwise their default values are used.
        New role paragraphs styles are defined:
            - their names in list 'roles'
            - their action is 'reply'
        Parameters
        ----------
        kwargs :    named parameters (== a dictionary)
            The definitions of overridden styles as dictionaries
            'roles' --> list of names of new role paragraph styles
        """
        # Define paragraph styles
        self.par_title = kwargs.get("title", TITLE)
        self.par_title_line = kwargs.get("title_line", TITLE_LINE)
        self.par_synopsis = kwargs.get("synopsis", SYNOPSIS)
        self.par_header = kwargs.get("header", HEADER)
        self.par_parenthesis = kwargs.get("parenthesis", PARENTHESIS)
        self.par_name = kwargs.get("name", NAME)
        self.par_reply = kwargs.get("reply", REPLY)

        self.text = ""
        self.previous = ""
        
        # Create own reply-method for each role
        for role in kwargs.get("roles", []):
            setattr(self, role, MethodType(self._role_template_function(role), self))

    def _role_template_function(self, role):
        def role_function(self, text):
            self.reply(role, text)
        return role_function

    def title(self, text_=""):
        self.text += format_text(text_, **self.par_title)
        self.previous = ""

    def title_line(self, text_=""):
        self.text += format_text(text_, **self.par_title_line)
        self.previous = ""

    def header(self, text_=""):
        self.text += format_text(text_, **self.par_header)
        self.previous = ""

    def synopsis(self, text_=""):
        self.text += format_text(text_, **self.par_synopsis)
        self.previous = ""

    def parenthesis(self, text_=""):
        self.text += format_text(text_, **self.par_parenthesis)
        self.previous = ""

    def name(self, text_=""):
        if self.previous.upper() != text_.upper():
            self.text += format_text(text_, **self.par_name)
            self.previous = text_
        else:
            self.text += "\n"

    def reply(self, name="", text_=""):
        if text_ != "":
            self.name(name)
        else:
            text_ = name
        self.text += format_text(text_, **self.par_reply)


if __name__ == "__main__":

    p = Book(roles=["franz", "josef"])

    p.title("Wienin Kevät")
    p.title_line()
    p.title_line("17.5.2019")
    p.title_line("Versio 1")
    p.title_line("Antero Kangas")
    p.title_line()

    p.synopsis(
        46*"-" +
        " "
        "Eletään 1800-luvun puoliväliä Wienissä. Kevät on kauneimmillaan, pikkulinnut visertävät "
        "ja aurinko paistaa kirk#kaas#ti pilvettömältä tai#vaalta. Ringstrassen kuu#lut katukahvilat "
        "ovat täynnä kauniista säästä nauttivia seu#ru#ei#ta. Itä#vallan säveltäjät luo#vat toinen "
        "tois#taan hienompia sävellyksiä. Eri#tyisesti Straussien valssit, polkat ja "
        "polkka-masurkat ovat val#loittaneet niin Itä#vallan kuin koko muun Eu#roopan."
    )
    p.synopsis(
        "Musiikin ja tanssiaisten suuret ystävät, her#rat Franz ja Josef, istuvat kahvilassa ja ovat"
        "mielipuuhassan, he nimittäin kiistelevät, kuin#ka ja missä polkka on syntynyt."
    )

    p.title_line(46*"-")

    p.parenthesis(
        "Keski-Eurooppalainen polkka on oikeasti se alkuperäinen The Polkka, josta suomalainen polkka syntyi " 
        "kansan kes#kuu#dessa. Tarina voi#daan kertoa joko niin, että herrat etsivät missä polkka on "
        "parhaimmillaan, tai he tutustu#vat eri#lai#siin polkkiin tai sitten tarina voidaan kir#joittaa kieli "
        "poskessa."
    )
    p.parenthesis(
        "Esimerkiksi: Polkka syntyi suomalaisen kansan kes#kuu#des#sa, ja sitä tanssittiin riihissä ja "
        "silloilla. Kun suo#ma#lai#set nuoret ylioppilaat lähtivät opiskelemaan Keski-Euroopan yli#opistoihin, "
        "kaipasivat he ylitse kai#ken suo#ma#laista saunaa sekä polkkaa. Saunaa oli vaikea jär#jes#tää, "
        "mutta he opettivat polk#kaa pai#kal#li#sil#le asukkail#le, niin että sitä alettiin tanssia "
        "kapakoissa ja maja#taloissa. Niistä sen huomasivat paikalliset aateliset, jotka pyy#si#vät "
        "tanssimestareitaan opettamaan sitä heil#le. Nämä tekivät työtä käskettyä, istuivat monta iltaa "
        "kapakoissa ja opettelivat polkkaa. Kui#ten#kin heidän mie#lestään se oli liian rahvaan#omaista, "
        "joten he ke#hit#ti#vät siitä mielestään hienostuneemman version, laukka#polkan."
    )

    p.parenthesis(
        "Herrat Josef ja Franz kiertävät ympäri Eu#roop#paa: Wie#nis#tä Pariisiin, sieltä Norjaan, "
        "sit#ten Suomeen Tam#pe#reel#le ja lopulta Lempäälään, jossa he saavat ihastella "
        "Lempäälän Peli#mannien vauhdikasta polkan soittoa. Matka käy läpi tanssisalien, konserttien, "
        "kesäjuhlien ja ope#ret#tien, he kuulevat mm. erilaisia valsseja sekä Feuer#festiä, "
        "Pas de Quatrea, Pariisin polkkaa ja lopulta suo#malaista Säkkijärven polkkaa."
    )

    p.header("I KOHTAUS: Kahvilassa")
    p.parenthesis(
        "Herrat Franz ja Josef ovat kävelyllä Wienin kuululla Ring#strassella. Kahvilasta kuuluu "
        "valssi-musiikkia. He py#säh#tyvät."
    )
    p.franz(
        "Tuohan kuulostaa kuin Johan Straussin, niiden kolmen kuuluisan säveltäjän isän, valssi-musiikilta. ")
    p.franz(
        "Eiköhän poiketa kahville kuun#te#lemaan ja nauttimaan siitä. Nytpäs me po#jat vie#täm#me#kin oi#kea#ta "
        "Pää-ääliö-öljy-yö-öykkäri-ilkiö-yötä!"
    )
    p.josef("No niinpäs kuulostaakin. Mennään vain.")
    p.franz("Taisimme erehtyä, musiikki onkin Pas d'Espagnea ja täällä alkavat ne kuuluisat Tanssiaiset.")
    p.josef(
        "Ei se mitään. Mutta emme taida ehtiä vielä juo#da kahvia, sillä "
        "meidän pitää hakea kauniit daamimme ja lähteä tanssimaan.")
    p.franz("Niinpä teemmekin. Hei, tulkaa kaikki tans#si#maan.")

    p.header("II KOHTAUS: Konsertissa")

    p.header("III KOHTAUS: Kesäjuhlissa")
    p.parenthesis("Franz ja Josef on kutsuttu kassakaappifirman kesä#juhliin.")
    p.josef("Wertheim-yhtiö kertoo myyneensä 20 000:nnen kassakaappinsa.")
    p.josef("Aika mahtava suoritus, eikös vaan?")

    p.franz(
        "Uskon kyllä, nehän ovat hyvin luotettavia ja kestäviä. Hehän järjestivät sen esityksenkin, "
        "jossa kaappia pidettiin tulessa melko pitkään. Kaappi ei mennyt rikki eivätkä sisällä olleet "
        "paperitkaan olleet palaneet."
    )
    p.josef("Ei siis mikään ihme, senkin Pää-ääliö-öljy-yö-öky-ilkiö, että he mainostavat tuotettaan tulen#kestäväksi.")
    p.franz("Juuri siksi meidänkin yhtiömme luottaa heidän kaappeihinsa.")
    p.josef(
        "Taidamme olla heille aika merkittävä asiakas, kutsuivathan he meidät mukaan firmansa kesä#juhliin. "
        "Hiukan huolestuttaa, kuulemani mukaan tuossa tilaisuudessa kaikki ovat tasa-arvoisia.")
    p.franz(
        "No mutta sehän on vain hienoa. Niin, ja kuu#lin, että tilasivat juhiinsa musiikki#teoksen "
        "itseltään Josef Straussilta.")
    p.josef(
        "Olen kuullut siitä, se on kuulemma polkkaa ja nimettykin tulenkestäväksi. "
        "Mennäänpä kuu#le#maan ja katsomaan Feuerfest!:iä")

    p.header("IV KOHTAUS: Pariisissa")

    p.header("V KOHTAUS: Huhuja")

    p.header("VI KOHTAUS: Lempäälässä")

    print(page_text(p.text))
