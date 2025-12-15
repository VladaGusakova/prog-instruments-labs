import csv
import re
from checksum import calculate_checksum, serialize_result

CSV_PATH = "77.csv"

REGEX = {
    "email": re.compile(
        r'\\w+@[a-z]+\\.[a-z]+(\\.[a-z]+)?'
    ),
    "http_status_message": re.compile(
        r'^\\d{3} [A-Za-z ]+$'
    ),
    "inn": re.compile(
        r'^\d{10}$|^\d{12}$'
    ),
    "passport": re.compile(
        r'\\d{2} \\d{2} \\d{6}'
    ),
    "ip_v4": re.compile(
        r'^((25[0-5]|2[0-4]\d|1?\d?\d)\.){3}'
        r'(25[0-5]|2[0-4]\d|1?\d?\d)$'
    ),
    "latitude": re.compile(
        r'^-?\d{1,2}\.\d+$'
    ),
    "hex_color": re.compile(
        r'#[a-fA-F0-9]{6}'
    ),
    "isbn": re.compile(
        r'^(\d{1,5}-){2,4}\d{1,7}-\d$'
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

    with open(path, encoding="utf-16") as file:
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
