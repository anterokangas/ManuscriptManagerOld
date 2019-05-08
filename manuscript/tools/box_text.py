
def box_text(text_lines, bc="+-+||+-+"):
    """
    Surround text block by a box
    :param text_lines: list of the textlines to be centered and boxed
    :param bc: boxing characters, indices as follows:
            011111112
            3 text  3
            3 lines 3
            455555556
    :return: string as above
    """
    print(f"box_text: {text_lines}")
    width = max([len(line) for line in text_lines])
    result = f"{bc[0]}{(width+2)*bc[1]}{bc[2]}"
    for line in text_lines:
        result +=f"\n{bc[3]} {line:^{width}} {bc[4]}"
    result += f"\n{bc[5]}{(width+2)*bc[6]}{bc[7]}"
    print(result)
    return result
