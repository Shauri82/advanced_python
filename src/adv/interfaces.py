from pathlib import Path
from typing import Protocol, Iterable, Iterator, Dict

from src.adv.model import AuctionKey, Auction, Vehicle


# Konrakt dla klasy przechowującej zbiór aukcji, umożliwia pobranie już istniejącej aukcji lub utworznie nowej, jeśli takiej jeszcze nie ma
class AuctionRepository(Protocol):
    def get_or_create(self, key: AuctionKey) -> Auction: ...


# Kontrakt dla klasy przetwarzającej dane dostarczane w formie słownika
class DataProcessor(Protocol):
    def process_rows(self, rows: Iterable[dict[str, str]]) -> list[Vehicle]: ...


# Konrakt dla klasy odczytującej dane i przetwarzającej je na słownik (może to być odczytywanie pliku csv ale w przyszłości też np. czytanie z bazy danych itp)
class RowReader(Protocol):
    def row_iterate(self, path: Path) -> Iterator[Dict[str, str]]: ...
