
import logging
import re

logger = logging.getLogger(__name__)


def cleanup_characters_from(string: str) -> str:
    """Cleans up a string from special characters and replaces them with
    their ASCII counterparts. It strips whitespaces from the beginning and
    the end of the string.

    e.g. "ä" -> "ae"
         " " -> "-"
         ...

    :param string: The string to clean up
    """
    if string:
        name = string.strip()
        for repl in [
            (" ", "-"),
            ("ä", "ae"),
            ("ö", "oe"),
            ("ü", "ue"),
            ("ß", "ss"),
            ("Ä", "Ae"),
            ("Ö", "Oe"),
            ("Ü", "Ue")
        ]:
            name = name.replace(*repl)
        name = re.sub(r"[^A-Za-z0-9\-.]", "", name)
        return name
    else:
        raise ValueError("CLEANUP EMPTY STRING...")
