from datetime import date, timedelta
from urllib.parse import parse_qs, urlparse

from app.config import settings
from app.schemas.recommendation import SearchParameters
from app.utils.stay22 import build_stay22_link, build_stay22_map_url

HOTEL = {"name": "Hotel Le Marais", "city": "Paris", "country": "France", "currency": "EUR"}


def _qs(url):
    parsed = urlparse(url)
    return parsed, {k: v[0] for k, v in parse_qs(parsed.query).items()}


def _future(days):
    return (date.today() + timedelta(days=days)).isoformat()


def test_link_has_aid_first_and_hotel_details():
    url = build_stay22_link(HOTEL, SearchParameters(location="Paris", adults=2))
    parsed, q = _qs(url)
    assert parsed.path == "/allez/roam"
    assert parsed.query.startswith("aid=testaid&")
    assert q["hotelname"] == "Hotel Le Marais"
    assert q["address"] == "Paris, France"
    assert q["adults"] == "2"
    assert q["currency"] == "EUR"
    assert q["campaign"] == "travelplanner_chat"


def test_link_includes_valid_future_dates():
    params = SearchParameters(check_in=_future(10), check_out=_future(13))
    _, q = _qs(build_stay22_link(HOTEL, params))
    assert q["checkin"] == params.check_in
    assert q["checkout"] == params.check_out


def test_link_drops_past_or_inverted_dates():
    for ci, co in [("2020-01-01", "2020-01-03"), (_future(5), _future(2)), ("bad", _future(3))]:
        _, q = _qs(build_stay22_link(HOTEL, SearchParameters(check_in=ci, check_out=co)))
        assert "checkin" not in q and "checkout" not in q


def test_link_falls_back_to_search_location():
    _, q = _qs(build_stay22_link({}, SearchParameters(location="Tokyo")))
    assert q["address"] == "Tokyo"
    assert "hotelname" not in q


def test_disabled_without_aid(monkeypatch):
    monkeypatch.setattr(settings, "stay22_aid", "")
    assert build_stay22_link(HOTEL, SearchParameters(location="Paris")) is None
    assert build_stay22_map_url(SearchParameters(location="Paris")) is None


def test_map_url():
    params = SearchParameters(
        location="Tokyo", check_in=_future(10), check_out=_future(12), adults=2, rooms=2
    )
    parsed, q = _qs(build_stay22_map_url(params))
    assert parsed.path == "/embed/gm"
    assert q["aid"] == "testaid"
    assert q["address"] == "Tokyo"
    assert q["campaign"] == "travelplanner_map"
    assert q["rooms"] == "2"
    assert q["checkin"] == params.check_in


def test_map_url_requires_location():
    assert build_stay22_map_url(SearchParameters()) is None
