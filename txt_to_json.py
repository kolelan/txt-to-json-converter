import json
import re
from pathlib import Path

# Конфигурация
COMPACT_MODE = True  # Если True - одна строка = один JSON-объект (в валидном массиве)
USE_SORT = True  # Если True - сортировать выходные данные
SORT_MODE = "key"  # "key" (по ключу) или "value" (по значению)


def parse_line(line: str) -> dict:
    """Разбирает строку формата 'KEY – VALUE' или 'KEY - VALUE' в словарь {KEY: VALUE}."""
    line = line.strip()
    if not line:
        return None

    parts = re.split(r"\s*[–-]\s*", line, maxsplit=1)
    if len(parts) != 2:
        print(f"⚠ Некорректный формат строки: '{line}'")
        return None

    key, value = parts[0].strip(), parts[1].strip()
    return {key: value}


def sort_data(data: list, sort_mode: str) -> list:
    """Сортирует список словарей по ключу или значению."""
    if sort_mode == "key":
        return sorted(data, key=lambda x: next(iter(x.keys())))
    elif sort_mode == "value":
        return sorted(data, key=lambda x: next(iter(x.values())))
    return data


def convert_txt_to_json(input_path: str, output_path: str) -> None:
    """Конвертирует .txt файл в .json с поддержкой компактного режима и сортировки."""
    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f"Файл '{input_path}' не найден!")

    parsed_data = []
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            if parsed_line := parse_line(line):
                parsed_data.append(parsed_line)

    # Сортировка (если включена)
    if USE_SORT:
        parsed_data = sort_data(parsed_data, SORT_MODE)

    output_file = Path(output_path)
    with open(output_file, "w", encoding="utf-8") as f:
        if COMPACT_MODE:
            # Компактный режим: валидный JSON-массив (одна строка = один объект)
            f.write("[\n")
            for i, item in enumerate(parsed_data):
                json.dump(item, f, ensure_ascii=False)
                if i < len(parsed_data) - 1:
                    f.write(",\n")
            f.write("\n]")
        else:
            # Стандартный режим: красивый JSON-массив
            json.dump(parsed_data, f, ensure_ascii=False, indent=4)

    print(f"✅ Успешно сохранено в {output_path} (COMPACT_MODE={COMPACT_MODE}, SORT={USE_SORT}, SORT_MODE={SORT_MODE})")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Использование: python txt_to_json_advanced.py входной_файл.txt выходной_файл.json")
        sys.exit(1)

    input_txt = sys.argv[1]
    output_json = sys.argv[2]

    try:
        convert_txt_to_json(input_txt, output_json)
    except Exception as e:
        print(f"❌ Ошибка: {e}")