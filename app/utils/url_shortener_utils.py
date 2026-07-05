import hashlib


def _create_checksum(url: str) -> str:
    """
    This function creates checksum for a given url

    Parameters
    ----------
    url: str
       The url which is sent for shortening

    checksum: str
      The final checksum first 10 digits.
    """
    checksum = hashlib.sha256(url.encode("utf-8")).hexdigest()
    return checksum[:10]
