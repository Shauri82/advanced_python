import asyncio
from pathlib import Path
from typing import List

from src.adv.csv_reader import DictDataProcessor, CsvRowReader
from src.adv.interfaces import AuctionRepository, DataProcessor, RowReader
from src.adv.model import AuctionMemoryCache, Vehicle
from src.adv.service import DataProcessingService


async def process_single_file_async(path: Path, processor: DataProcessingService) -> list[Vehicle]:
    print(f"... przetwarzam: {path.name}...")

    loop = asyncio.get_running_loop()
    results = await loop.run_in_executor(
        None,
        sync_work,
        path, processor
    )

    print(f"Zakończono przetwarzanie {path.name}: {len(results)} pojazdów")
    return results


def sync_work(path: Path, processor: DataProcessingService) -> list[Vehicle]:
    return processor.process_source(path)


async def process_multiple_files_async(file_paths: List[Path], processor: DataProcessingService) -> List[Vehicle]:
    tasks = [process_single_file_async(path, processor) for path in file_paths]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    all_vehicles = []
    for result in results:
        if isinstance(result, Exception):
            print(f"Błąd: {result}")
        else:
            all_vehicles.extend(result)

    return all_vehicles


def create_dependencies() -> DataProcessingService:
    cache: AuctionRepository = AuctionMemoryCache()
    processor: DataProcessor = DictDataProcessor(cache)
    row_reader: RowReader = CsvRowReader()
    return DataProcessingService(processor, row_reader)


# --------------------------------------------------------------------
# Przetwarzanie plików :

data_dir = Path("../data")
csv_files: list[Path] = [
    data_dir / "Sales_List_03042024 (12).csv",
    data_dir / "Sales_List_03052025 (24).csv",
    data_dir / "Sales_List_04032025 (11).csv",
    data_dir / "Sales_List_07092024 (35).csv",
    data_dir / "Sales_List_09032025 (17).csv",
    data_dir / "Sales_List_09032025 (20).csv",
    data_dir / "Sales_List_10082024 (20).csv",
    data_dir / "Sales_List_10102025 (12).csv",
    data_dir / "Sales_List_10102025 (16).csv",
    data_dir / "Sales_List_10312025 (4).csv",
    data_dir / "Sales_List_10312025 (11).csv",
    data_dir / "Sales_List_12012025 (3).csv",
    data_dir / "Sales_List_12012025 (11).csv",
    data_dir / "Sales_List_12012025 (22).csv",
    data_dir / "Sales_List_12092025 (3).csv",
    data_dir / "Sales_List_12092025 (16).csv",
]

service = create_dependencies()

vehicles = asyncio.run(process_multiple_files_async(csv_files, service))
print(f"Przetworzono {len(vehicles)} pojazdów z {len(csv_files)} plików")
