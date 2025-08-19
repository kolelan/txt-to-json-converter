import json


def json_to_txt(input_file, output_file, convert_type='field', field_to_extract='name', sort_output=False):
    try:
        # Чтение JSON-файла
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Проверка, что данные являются массивом объектов
        if not isinstance(data, list):
            raise ValueError("JSON должен содержать массив объектов")

        extracted_data = []

        for item in data:
            if not isinstance(item, dict):
                raise ValueError("Каждый элемент массива должен быть объектом (dict)")

            if convert_type == 'key':
                # Проверяем, что объект содержит ровно одну пару ключ-значение
                if len(item) != 1:
                    raise ValueError(
                        "Для convert_type='key' каждый объект должен содержать ровно одну пару ключ-значение")
                extracted_data.append(next(iter(item.keys())))

            elif convert_type == 'value':
                # Проверяем, что объект содержит ровно одну пару ключ-значение
                if len(item) != 1:
                    raise ValueError(
                        "Для convert_type='value' каждый объект должен содержать ровно одну пару ключ-значение")
                extracted_data.append(next(iter(item.values())))

            elif convert_type == 'field':
                if field_to_extract in item:
                    extracted_data.append(str(item[field_to_extract]))
                else:
                    raise ValueError(f"Поле '{field_to_extract}' отсутствует в одном из объектов")

            else:
                raise ValueError(f"Неизвестный convert_type: {convert_type}")

        # Сортировка при необходимости
        if sort_output:
            extracted_data.sort()

        # Запись в текстовый файл
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(extracted_data))

        print(f"Успешно обработано {len(extracted_data)} элементов")
        return True

    except json.JSONDecodeError:
        print("Ошибка: Файл не является валидным JSON")
    except ValueError as ve:
        print(f"Ошибка преобразования: {ve}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")

    return False


if __name__ == "__main__":
    # Конфигурационные параметры
    config = {
        'input_file': 'kaponir-api/classes_no_desc.json',
        'output_file': 'kaponir-api/classes_no_desc.txt',
        'convert_type': 'key',  # 'key', 'value' или 'field'
        'field_to_extract': 'name',  # Используется только при convert_type='field'
        'sort_output': True  # Сортировать ли результат
    }

    # Запуск преобразования
    json_to_txt(
        input_file=config['input_file'],
        output_file=config['output_file'],
        convert_type=config['convert_type'],
        field_to_extract=config['field_to_extract'],
        sort_output=config['sort_output']
    )