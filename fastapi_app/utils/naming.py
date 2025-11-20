import re


def camel_case_to_snake_case(input_str: str) -> str:
    """
    Convert CamelCase → snake_case with correct handling of abbreviations.
    """
    chars = []
    for c_idx, char in enumerate(input_str):
        if c_idx and char.isupper():
            nxt_idx = c_idx + 1
            flag = nxt_idx >= len(input_str) or input_str[nxt_idx].isupper()
            prev_char = input_str[c_idx - 1]
            if prev_char.isupper() and flag:
                pass
            else:
                chars.append("_")
        chars.append(char.lower())
    return "".join(chars)


def pluralize(word: str) -> str:
    """
    English pluralization for table names.
    """
    # box → boxes, match → matches, class → classes
    if re.search(r'(s|x|z|ch|sh)$', word):
        return word + "es"

    # category → categories (but toy → toys, key → keys)
    if word.endswith("y") and not re.search(r'[aeiou]y$', word):
        return word[:-1] + "ies"

    return word + "s"


def make_tablename(cls) -> str:
    """
    Convert a model class name to a table name:
    CamelCase → snake_case → plural
    """
    snake = camel_case_to_snake_case(cls.__name__)
    return pluralize(snake)
