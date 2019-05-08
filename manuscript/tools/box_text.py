
def box_text(text_lines, bc="+-+||+-+"):
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
        text_lines = [line.strip() for line in text_lines.split("\n")]

    width = max([len(line) for line in text_lines])

    result = f"{bc[0]}{(width+2)*bc[1]}{bc[2]}"
    for line in text_lines:
        result += f"\n{bc[3]} {line:^{width}} {bc[4]}"
    result += f"\n{bc[5]}{(width+2)*bc[6]}{bc[7]}"

    return result
