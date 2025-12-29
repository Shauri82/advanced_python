import csv
from pathlib import Path
from typing import Iterable, Iterator, Dict

from src.adv.interfaces import DataProcessor, AuctionRepository, RowReader
from src.adv.model import Vehicle, AuctionKey
from src.adv.parser import parse_auction_datetime


class CsvRowReader(RowReader):
    def row_iterate(self, path: Path) -> Iterator[Dict[str, str]]:
        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield row


def make_auction_key(row: Dict[str, str]) -> AuctionKey:
    return AuctionKey(
        date=parse_auction_datetime(row["Auction Date"]),
        city=row["Branch Name"],
    )


# Klasa do przetwarzania danych w słowniku na obiekty typu Vehicle
class DictDataProcessor(DataProcessor):
    def __init__(self, auction_repo: AuctionRepository):
        self._auction_repo = auction_repo

    def process_rows(self, rows: Iterable[dict[str, str]]) -> list[Vehicle]:
        vehicles: list[Vehicle] = []

        for row in rows:
            key = make_auction_key(row)
            auction = self._auction_repo.get_or_create(key)
            vehicle = Vehicle(
                stock_number=row["Stock Number"],
                year=int(row["Year"]),
                make=row["Make"],
                model=row["Model"],
                vehicle_type=row["Vehicle Type"],
                auction=auction,
            )
            vehicles.append(vehicle)

        return vehicles
