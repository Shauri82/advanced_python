import threading
from dataclasses import dataclass
from datetime import datetime
from typing import NamedTuple, Dict


@dataclass(frozen=True)
class Auction:
    date: datetime
    city: str


@dataclass(frozen=True)
class Vehicle:
    stock_number: str
    year: int
    make: str
    model: str
    vehicle_type: str
    auction: Auction


# Klasa pomocnicza na potrzeby cache'a aukcji. NamedTuple zapewnia hashable
class AuctionKey(NamedTuple):
    date: datetime
    city: str


# Klasa implementująca kontrakt AuctionRepository. Pole _lock zapewnia atomowy dostęp do słownika
class AuctionMemoryCache:
    def __init__(self):
        self._auction_cache: Dict[AuctionKey, Auction] = {}
        self._lock = threading.Lock()

    def get_or_create(self, key: AuctionKey) -> Auction:
        with self._lock:
            if key not in self._auction_cache:
                self._auction_cache[key] = Auction(date=key.date, city=key.city)
            return self._auction_cache[key]
