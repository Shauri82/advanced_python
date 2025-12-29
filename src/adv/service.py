from pathlib import Path

from src.adv.interfaces import DataProcessor, RowReader
from src.adv.model import Vehicle

# Serwis przetwarzający dane na listę pojazdów.
class DataProcessingService:
    def __init__(self, data_processor: DataProcessor, row_reader: RowReader):
        self._data_processor = data_processor
        self._row_reader = row_reader

    def process_source(self, path: Path) -> list[Vehicle]:
        rows = self._row_reader.row_iterate(path)
        return self._data_processor.process_rows(rows)
