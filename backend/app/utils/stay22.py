"""
Stay22 Allez deep-link builder.

Docs: https://dev.stay22.com/docs/allez/parameters

Builds an affiliate link that sends the user to the best OTA (``/allez/roam``)
with the hotel and the user's search pre-filled, attributed to our AID.
"""
from datetime import date
from typing import Any, Dict, Optional
from urllib.parse import urlencode

from app.config import settings
from app.schemas.recommendation import SearchParameters

ALLEZ_BASE_URL = "https://www.stay22.com/allez"
MAP_EMBED_URL = "https://www.stay22.com/embed/gm"


def _valid_date_range(check_in: Optional[str], check_out: Optional[str]) -> bool:
    """Stay22 needs both dates, ISO formatted, not in the past, checkout > checkin."""
    if not check_in or not check_out:
        return False
    try:
        ci = date.fromisoformat(check_in)
        co = date.fromisoformat(check_out)
    except ValueError:
        return False
    return date.today() <= ci < co


def build_stay22_link(
    hotel: Dict[str, Any],
    params: SearchParameters,
    campaign: Optional[str] = None,
) -> Optional[str]:
    """
    Return a Stay22 Allez link for ``hotel``, or None if no AID is configured.

    ``aid`` is placed first in the query string, as Stay22 recommends.
    """
    aid = settings.stay22_aid.strip()
    if not aid:
        return None

    query: Dict[str, Any] = {"aid": aid}

    if hotel.get("name"):
        query["hotelname"] = hotel["name"]

    # City + country gives the best fuzzy-match accuracy; fall back to the searched location.
    address = ", ".join(p for p in (hotel.get("city"), hotel.get("country")) if p) or params.location
    if address:
        query["address"] = address

    if _valid_date_range(params.check_in, params.check_out):
        query["checkin"] = params.check_in
        query["checkout"] = params.check_out

    if params.adults:
        query["adults"] = params.adults
    if params.children:
        query["children"] = params.children

    if hotel.get("currency"):
        query["currency"] = hotel["currency"]

    campaign = campaign or settings.stay22_campaign
    if campaign:
        query["campaign"] = campaign

    provider = settings.stay22_provider or "roam"
    return f"{ALLEZ_BASE_URL}/{provider}?{urlencode(query)}"


def build_stay22_map_url(
    params: SearchParameters,
    campaign: Optional[str] = None,
) -> Optional[str]:
    """
    Return a Stay22 map embed URL for the searched destination, or None if
    there is no AID or no location to centre the map on.

    Docs: https://dev.stay22.com/docs/maps/parameters
    """
    aid = settings.stay22_aid.strip()
    if not aid or not params.location:
        return None

    query: Dict[str, Any] = {
        "aid": aid,
        "address": params.location,
        "zoom": 13,  # city-level; Stay22 default (16) is street-level
        "maincolor": "ff6b6b",  # site accent (--accent-orange)
        "campaign": campaign or settings.stay22_map_campaign,
    }

    if _valid_date_range(params.check_in, params.check_out):
        query["checkin"] = params.check_in
        query["checkout"] = params.check_out

    if params.adults:
        query["adults"] = params.adults
    if params.children:
        query["children"] = params.children
    if params.rooms and params.rooms > 1:
        query["rooms"] = params.rooms

    return f"{MAP_EMBED_URL}?{urlencode(query)}"
