# tests/test_csv_reader.py
from datetime import datetime
from unittest.mock import Mock
from zoneinfo import ZoneInfo

import pytest

from src.adv.csv_reader import DictDataProcessor
from src.adv.interfaces import AuctionRepository
from src.adv.model import Auction


@pytest.fixture
def mock_repo():
    repo = Mock(spec=AuctionRepository)
    auction = Auction(
        date=datetime(2025, 3, 4, 8, 30, tzinfo=ZoneInfo('America/Chicago')),
        city="New Castle"
    )
    repo.get_or_create.return_value = auction
    return repo


@pytest.fixture
def csv_row_data():
    return {
        "Stock Number": "38395072",
        "Year": "2015",
        "Make": "GMC",
        "Model": "ACADIA",
        "Vehicle Type": "SUVs",
        "Auction Date": "Mon Mar 04, 8:30am CST",
        "Branch Name": "New Castle",
    }


def test_dict_processor_creates_vehicle_from_csv_row(csv_row_data, mock_repo):
    processor = DictDataProcessor(mock_repo)
    vehicles = processor.process_rows([csv_row_data])

    assert len(vehicles) == 1
    vehicle = vehicles[0]

    assert vehicle.stock_number == "38395072"
    assert vehicle.year == 2015
    assert vehicle.make == "GMC"
    assert vehicle.model == "ACADIA"
    assert vehicle.vehicle_type == "SUVs"

    called_key = mock_repo.get_or_create.call_args[0][0]
    assert called_key.city == "New Castle"
    assert called_key.date.tzinfo.key == "America/Chicago"
