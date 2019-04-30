from typing import Any, Dict

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets
from logzero import logger
import requests

__all__ = ["ask_for_supower", "has_kept_superpower"]
# horrible global vars
fetched_superpowers = []
session = None


def ask_for_superpower(service_url: str, timeout: int = 3,
                       configuration: Configuration = None, 
                       secrets: Secrets = None) -> Dict[str, Any]:
    """
    Fetch a superpower
    """
    global session
    if not session:
        session = requests.Session()

    headers = {
        'Accept': 'application/json'
    }

    info = {}
    try:
        r = session.get(
            service_url, headers=headers, timeout=(timeout, timeout))
    except requests.exceptions.Timeout as x:
        logger.warning("Superpowers were too slow to arrive!")
        return False

    if r.status_code == 200:
        info = r.json()
        fetched_superpowers.append(info)

    return {
        "status": r.status_code,
        "headers": dict(**r.headers),
        "body": info
    }


def has_kept_superpower(configuration: Configuration = None,
                        secrets: Secrets = None) -> bool:
    """
    Check two calls to `ask_for_superpower` have resulted in the same returned
    superpower.
    """
    if len(fetched_superpowers) <= 1:
        return True

    global session
    if session:
        session.close()
        session = None

    return fetched_superpowers[0]['name'] == \
        fetched_superpowers[-1]['name']
