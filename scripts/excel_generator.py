"""Script to generate en excel file from the AWS massive dataset."""
from enum import Enum
from typing import Any, Dict, Optional

import httpx
import xlsxwriter


class ExcelFileWriter:
    """ExcelFileWriter class."""

    _workbook: xlsxwriter.Workbook
    _cell_formats: Dict[str, Any]
    _sheets: Dict[str, Any]

    def __init__(self, workbook_name: str) -> None:
        """Class constructor."""
        self._workbook = xlsxwriter.Workbook(filename=workbook_name)
        self._sheets = {}
        self._cell_formats = {}

    def add_worksheet(self, name: str) -> None:
        """Add a worksheet to the workbook."""
        self._sheets[name] = self._workbook.add_worksheet(name)

    def create_format(self, cell_format: Dict[str, Any]) -> None:
        """Add a format to the workbook."""
        for format_name, _ in cell_format.items():
            self._cell_formats[format_name] = self._workbook.add_format(cell_format)

    def write(  # pylint: disable=R0913
        self,
        sheet: str,
        row: int,
        col: int,
        text: str,
        cell_format: Optional[str] = None,
    ) -> None:
        """Write information into in the workbook."""
        if cell_format:
            self._sheets[sheet].write(row, col, text, self._cell_formats[cell_format])
            return None

        self._sheets[sheet].write(row, col, text)

        return None

    def close(self) -> None:
        """Close the inmenory workbook."""
        self._workbook.close()


def fetch_json_data(url: str) -> Dict[str, Any]:
    """Fetch json data from an url."""
    with httpx.Client() as client:
        response = client.get(url=url)

    data = response.json()

    return data


class FileColumns(Enum):
    """Excel file columns enum."""

    Category = 0
    Text = 1


if __name__ == "__main__":
    workbook_name = "corpus-massive-es.xlsx"
    sheet_name = "Textos"
    url = (
        "https://raw.githubusercontent.com/jesus-seijas-sp/fastest_nlu/main/benchmark/corpus-massive-es.json"
    )

    file_writer = ExcelFileWriter(workbook_name=workbook_name)

    file_writer.add_worksheet(name=sheet_name)
    file_writer.write(sheet=sheet_name, col=FileColumns.Category.value, row=0, text=FileColumns.Category.name)
    file_writer.write(sheet=sheet_name, col=FileColumns.Text.value, row=0, text=FileColumns.Text.name)

    data = fetch_json_data(url=url)

    row_index = 1
    for data_chunk in data["data"]:
        category_name = data_chunk["intent"]

        for text in data_chunk["utterances"]:
            file_writer.write(
                sheet=sheet_name, row=row_index, col=FileColumns.Category.value, text=category_name
            )
            file_writer.write(sheet=sheet_name, row=row_index, col=FileColumns.Text.value, text=text)
            row_index += 1

        for text in data_chunk["tests"]:
            file_writer.write(
                sheet=sheet_name, row=row_index, col=FileColumns.Category.value, text=category_name
            )
            file_writer.write(sheet=sheet_name, row=row_index, col=FileColumns.Text.value, text=text)
            row_index += 1

    file_writer.close()
