from math import log10

def format_number(i: int, total: int, zero_indexed=True) -> str:
    """ Format a number to have the right number of leading zero for a nice
    ordering.

    Parameters
    ----------
    i: int
        value to convert to a str
    total: int
        max value to convert

    Examples
    --------
    >>> format_number(1, 100)
    '01'
    >>> format_number(1, 100, zero_indexed=False)
    '001'
    """
    if zero_indexed:
        total = total - 1
    if total < 1:
        return f"{i}"
    return f"{i:0{int(log10(total)) + 1}}"
