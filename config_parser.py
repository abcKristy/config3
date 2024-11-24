import re
import yaml
import sys

# Регулярные выражения для поиска шаблонов
CONST_PATTERN = r"(\w+)\s*=\s*(.+?);"
CONST_REF_PATTERN = r"\$(\w+)\$"
COMMENT_PATTERN = r"\{#.*?#\}"
KEY_VALUE_PATTERN = r"(\w+)\s*:=\s*(.+?);"
ARRAY_PATTERN = r"\[([\s\S]+?)\]"
DICT_PATTERN = r"begin\s([\s\S]+?)end"
NUMBER_PATTERN = r"^\d+$"
STRING_PATTERN = r'^".*"$'

class ConfigParser:
    def __init__(self):
        self.constants = {}

    def parse(self, input_text):
        input_text = self._remove_comments(input_text)
        self._process_constants(input_text)
        yaml_structure = self._process_structure(input_text)
        return yaml.dump(yaml_structure, allow_unicode=True)

    def _remove_comments(self, text):
        return re.sub(COMMENT_PATTERN, "", text, flags=re.DOTALL)

    def _process_constants(self, text):
        matches = re.findall(CONST_PATTERN, text)
        for name, value in matches:
            if re.match(NUMBER_PATTERN, value):
                self.constants[name] = int(value)
            elif re.match(STRING_PATTERN, value):
                self.constants[name] = value.strip('"')
            else:
                raise SyntaxError(f"Invalid constant value: {value}")

    def _replace_constants(self, text):
        def replace(match):
            const_name = match.group(1)
            if const_name not in self.constants:
                raise SyntaxError(f"Undefined constant: {const_name}")
            return str(self.constants[const_name])

        return re.sub(CONST_REF_PATTERN, replace, text)

    def _process_structure(self, text):
        text = self._replace_constants(text)
        dict_matches = re.findall(DICT_PATTERN, text, flags=re.DOTALL)
        result = []
        for dict_match in dict_matches:
            parsed_dict = {}
            key_value_matches = re.findall(KEY_VALUE_PATTERN, dict_match)
            for key, value in key_value_matches:
                print(f"Processing key: {key}, value: {value}")  # Отладка
                parsed_dict[key] = self._parse_value(value)
            result.append(parsed_dict)
        return result

    def _parse_value(self, value):
        value = value.strip()
        print(f"Parsing value: {value}")  # Отладочный вывод
        if re.match(STRING_PATTERN, value):  # Сначала проверяем строки
            return value.strip('"')  # Убираем кавычки
        elif re.match(NUMBER_PATTERN, value):  # Затем числа
            return int(value)
        elif re.match(ARRAY_PATTERN, value):  # Затем массивы
            array_items = re.findall(ARRAY_PATTERN, value)[0].strip().split()
            return [self._parse_value(item) for item in array_items]
        elif re.match(DICT_PATTERN, value, flags=re.DOTALL):  # Затем словари
            return self._process_structure(value)
        else:
            raise SyntaxError(f"Invalid value: {value}")

# Основная функция
def main():
    if len(sys.argv) != 2:
        print("Usage: python config_parser.py <path_to_config>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            input_text = f.read()

        parser = ConfigParser()
        yaml_output = parser.parse(input_text)
        print(yaml_output)

    except FileNotFoundError:
        print(f"Error: File '{config_file}' not found.")
        sys.exit(1)
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()