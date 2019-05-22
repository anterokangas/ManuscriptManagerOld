import manuscript.tools.constants as mc


def box_text(text_lines, bc="+-+||+-+", keep=False, min_width=1):
    """
    Surround text block by a box
    :param text_lines: list of the textlines to be centered and boxed OR
           string of lnes separated by \n: lines are first listed and stripped
    :param bc: boxing characters, indices as follows:
            011111112
            3 text  3
            3 lines 3
            455555556
    :return: string as above
    """
    if isinstance(text_lines, str):
        if keep:
            text_lines = [line.strip("\n") for line in text_lines.split("\n")]
            align_code = ""
        else:
            text_lines = [line.strip() for line in text_lines.split("\n")]
            align_code = "^"
    width = max(max([len(line) for line in text_lines]), min_width)
    result = f"{bc[0]}{(width+2)*bc[1]}{bc[2]}"
    for line in text_lines:
        result += f"\n{bc[3]} {line:{align_code}{width}} {bc[4]}"
    result += f"\n{bc[5]}{(width+2)*bc[6]}{bc[7]}"

    return result


def page_text(text_lines, page_length=mc.PAGE_LENGTH, form_feed=True):
    page_number = 1
    text_lines = [line.strip("\n") for line in text_lines.split("\n")]
    width = max(max([len(line) for line in text_lines]), mc.PAGE_WIDTH)
    line_number = 1
    footer = "\n{:^" + str(width) + "}"
    result = ""
    page = ""
    page_number = 1
    for line in text_lines:
        if line_number <= page_length - 2:
            page += line + "\n"
            line_number += 1
        else:
            page += footer.format("- "+str(page_number)+" -")
            result += box_text(page, keep=True, min_width=width) + "\n"
            if form_feed:
                result += "\x0c\n"
            page = ""
            line_number = 1
            page_number += 1
    for _ in range(line_number, page_length-2):
        page += " \n"
    page += footer.format("- " + str(page_number) + " -")
    result += box_text(page, keep=True, min_width=width) + "\n"

    return result



