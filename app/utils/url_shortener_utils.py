import hashlib


def _create_short_code(url: str) -> str:
    """
    This function creates short_code for a given url

    Parameters
    ----------
    url: str
       The url which is sent for shortening

    short_code: str
      The final short_code first 10 digits.
    """
    short_code = hashlib.sha256(url.encode("utf-8")).hexdigest()
    return short_code[:10]
