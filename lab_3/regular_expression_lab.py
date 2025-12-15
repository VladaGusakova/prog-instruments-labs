import csv
import re
from typing import List
from checksum import calculate_checksum, serialize_result

CSV_PATH = "77.csv"

REGEX = {
    "email": r'^\w+@\w+\.\w+$',
    "http_status_message": r'^\d{3} [A-Za-z ]+$',
    "inn": r'^\d{10}$|^\d{12}$',
    "passport": r'^\d{2} \d{2} \d{6}$',
    "ip_v4": r'^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$',
    "latitude": r'^-?(?:90(?:\.0+)?|[0-8]?\d(?:\.\d+)?)$',
    "hex_color": r'^#[A-Fa-f0-9]{6}$',
    "isbn": r'^\d+-\d+-\d+-\d+(?:-\d+)?$',
    "uuid": r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
    "time": r'^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d\.\d{6}$',
}


def find_invalid_rows(file_path: str, encoding: str = "utf-16", delimiter: str = ";") -> List[int]:
    invalid_rows = []

    with open(file_path, "r", encoding=encoding) as f:
        reader = csv.DictReader(f, delimiter=delimiter)

        for row_index, row in enumerate(reader):
            for column, pattern in REGEX.items():
                value = row.get(column, "") or ""
                value = value.strip().strip('"')
                if not re.fullmatch(pattern, value):
                    invalid_rows.append(row_index)
                    break

    return sorted(set(invalid_rows))


def main() -> None:
    invalid_rows = find_invalid_rows(CSV_PATH)
    checksum = calculate_checksum(invalid_rows)
    print(checksum)
    serialize_result(77, checksum)


if __name__ == "__main__":
    main()