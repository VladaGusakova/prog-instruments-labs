import csv
import re
from checksum import calculate_checksum, serialize_result

CSV_PATH = "77.csv"


REGEX = {
    '\ufeff"email"': re.compile(
        r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    ),
    "http_status_message": re.compile(
        r'^\d{3} [A-Za-z ]+$'
    ),
    "inn": re.compile(
        r'^\d{10}$|^\d{12}$'
    ),
    "passport": re.compile(
        r'^\d{2} \d{2} \d{6}$'
    ),
    "ip_v4": re.compile(
        r'^(?:\d{1,3}\.){3}\d{1,3}$'
    ),
    "latitude": re.compile(
        r'^-?(?:[0-8]?\d(?:\.\d+)?|90(?:\.0+)?)$'
    ),
    "hex_color": re.compile(
        r'^#[0-9a-fA-F]{6}$'
    ),
    "isbn": re.compile(
        r'^(?:\d-){3}\d-\d{3}-\d$|^(?:\d-){4}\d-\d$'
    ),
    "uuid": re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    ),
    "time": re.compile(
        r'^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d\.\d{6}$'
    ),
}

def find_invalid_rows(path: str) -> list[int]:
    invalid_rows = []

    with open(path, encoding="utf-16-le") as file:
        reader = csv.DictReader(file, delimiter=";")

        for row_index, row in enumerate(reader):
            for column, pattern in REGEX.items():
                if not pattern.fullmatch(row[column]):
                    invalid_rows.append(row_index)
                    break

    return invalid_rows

def main() -> None:
    invalid_rows = find_invalid_rows(CSV_PATH)
    checksum = calculate_checksum(invalid_rows)
    print(checksum)
    serialize_result(77, checksum)


if __name__ == "__main__":
    main()
