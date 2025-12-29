from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from src.adv.parser import parse_auction_datetime


class TestParseAuctionDatetime:
    @pytest.mark.parametrize("raw,expected_hour,expected_minute,expected_tz", [
        ("Tue Dec 09, 8:30am CST", 8, 30, "America/Chicago"),
        ("Tue Dec 09, 1:06am CDT", 1, 6, "America/Chicago"),
        ("Mon Jan 15, 3:45pm EST", 15, 45, "America/New_York"),
        ("Fri Dec  5, 2:15am PST", 2, 15, "America/Los_Angeles"),
        ("Tue Dec 09, 8:30am CEDT", 8, 30, "Europe/Warsaw"),
        ("Wed Nov 12, 11:00pm CEST", 23, 0, "Europe/Warsaw"),
    ])
    def test_valid_formats(self, raw: str, expected_hour: int, expected_minute: int, expected_tz: str):
        result = parse_auction_datetime(raw)
        assert result.hour == expected_hour
        assert result.minute == expected_minute
        assert str(result.tzinfo) == expected_tz
        assert result.year == datetime.now().year

    @pytest.mark.parametrize("raw", [
        "Tue Dec 09, 8:30am cst",
        "  Tue Dec 09, 8:30am CST  ",
        "Fri Dec  5, 2:15am CST",
    ])
    def test_zone_edge_cases(self, raw: str):
        result = parse_auction_datetime(raw)
        assert result.tzinfo is not None
        assert isinstance(result.tzinfo, ZoneInfo)

    @pytest.mark.parametrize("invalid_raw", [
        "", "invalid", "2025-01-01", "Tue Dec 09", "Tue Dec 09, 8:30am"
    ])
    def test_invalid_format_raises(self, invalid_raw):
        with pytest.raises(ValueError, match="Nieobsługiwany format daty"):
            parse_auction_datetime(invalid_raw)

    @pytest.mark.parametrize("raw,tz_error", [
        ("Tue Dec 09, 8:30am XXX", "XXX"),
        ("Tue Dec 09, 8:30am ZZZ", "ZZZ"),
    ])
    def test_unknown_tz_raises(self, raw: str, tz_error: str):
        with pytest.raises(ValueError, match=f"Nieznana strefa czasowa: {tz_error}"):
            parse_auction_datetime(raw)
