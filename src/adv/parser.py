import re
from datetime import datetime
from zoneinfo import ZoneInfo

TIMEZONE_MAP = {
    "CST": ZoneInfo("America/Chicago"),
    "CDT": ZoneInfo("America/Chicago"),
    "EST": ZoneInfo("America/New_York"),
    "EDT": ZoneInfo("America/New_York"),
    "PST": ZoneInfo("America/Los_Angeles"),
    "PDT": ZoneInfo("America/Los_Angeles"),
    "CET": ZoneInfo("Europe/Warsaw"),
    "CEST": ZoneInfo("Europe/Warsaw"),
    "CEDT": ZoneInfo("Europe/Warsaw"),
}

PATTERN = re.compile(
    r"(?P<date>\w{3} \w{3} \d{1,2}, \d{1,2}:\d{2}[ap]m)\s+(?P<tz>\w+)",
    re.IGNORECASE
)


def parse_auction_datetime(raw: str) -> datetime:
    raw = re.sub(r"\s+", " ", raw.strip())
    match = PATTERN.search(raw)

    if not match:
        raise ValueError(f"Nieobsługiwany format daty: {raw}")

    date_part = match.group("date")
    tz_abbr = match.group("tz").upper()

    date_and_time = datetime.strptime(date_part, "%a %b %d, %I:%M%p")

    date_and_time = date_and_time.replace(year=datetime.now().year)

    tzinfo = TIMEZONE_MAP.get(tz_abbr)
    if not tzinfo:
        raise ValueError(f"Nieznana strefa czasowa: {tz_abbr}")

    return date_and_time.replace(tzinfo=tzinfo)
