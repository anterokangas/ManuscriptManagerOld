
def print_list(header=None, the_list=[], numbers=True):
    """ Print List by elements
        ----------------------
    :param header: if not None then printed before list
    :param the_list: to be printed
    :param numbers: bool should lines be numebered or not
    :return: None
    """
    if heaer is not None:
        print(header)
    num_len = len(str(len(the_list)))
    for ielement, element in enumerate(the_list):
        if numbers:
            print(f"{ielement:{num_len}}   {element}")
        else:
            print(f"   {element}")