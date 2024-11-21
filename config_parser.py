import re
import yaml

# Регулярные выражения для поиска шаблонов
CONST_PATTERN = r"(\w+)\s*=\s*(.+?);"
CONST_REF_PATTERN = r"\$(\w+)\$"
COMMENT_PATTERN = r"\{#.*?#\}"
KEY_VALUE_PATTERN = r"(\w+)\s*:=\s*(.+?);"
ARRAY_PATTERN = r"\[([\s\S]+?)\]"
DICT_PATTERN = r"begin\s([\s\S]+?)end"
NUMBER_PATTERN = r"^\d+$"
STRING_PATTERN = r"^\".*\"$"

class ConfigParser:
    def __init__(self):
        self.constants = {}  # Инициализация словаря для хранения констант

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
                parsed_dict[key] = self._parse_value(value)
            result.append(parsed_dict)

        return result

    def _parse_value(self, value):
        value = value.strip()
        if re.match(NUMBER_PATTERN, value):
            return int(value)
        elif re.match(STRING_PATTERN, value):
            return value.strip('"')
        elif re.match(ARRAY_PATTERN, value):
            return [self._parse_value(item) for item in re.split(r"\s+", re.findall(ARRAY_PATTERN, value)[0])]
        elif re.match(DICT_PATTERN, value, flags=re.DOTALL):
            return self._process_structure(value)
        else:
            raise SyntaxError(f"Invalid value: {value}")