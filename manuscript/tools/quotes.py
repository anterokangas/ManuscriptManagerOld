
def add_quotes(text_, always=False):
    if " " not in text_ and not always:
        # No need to add quotes
        return text_
    if '"' not in text_:
        return '"' + text_ + '"'
    if "'" not in text_:
        return "'" + text_ +"'"
    # Error
    raise ValueError(f"*** Cannot add quotes to string {text_}")


def remove_quotes(text_):
    if len(text_) < 2:
        return text_
    if text_[0] == text_[-1] == "'" \
       or text_[0] == text_[-1] == '"':
        return text_[1:-1]
    return text_
