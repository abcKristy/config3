import sys
import re
import yaml
import traceback
from collections import OrderedDict

CONST_PATTERN = r"(\w+)\s*=\s*(.+?);"
CONST_REF_PATTERN = r"\$(\w+)\$"
COMMENT_PATTERN = r"\{#.*?#\}"
KEY_VALUE_PATTERN = r"(\w+)\s*:=\s*(.+?);"
ARRAY_PATTERN = r"\[([\s\S]+?)\]"
DICT_PATTERN = r"begin\s([\s\S]+?)\send"
NUMBER_PATTERN = r"^\d+$"
STRING_PATTERN = r'^"(.*?)"$'


class ConfigParser:
    def __init__(self):
        self.constants = {}

    def parse(self, input_text, filename="<string>"):
        try:
            input_text = self._remove_comments(input_text)
            self._process_constants(input_text)
            input_text = self._replace_constants(input_text)
            yaml_structure = self._process_structure(input_text, filename)
            return yaml.dump(yaml_structure, default_flow_style=False, allow_unicode=True, indent=2)
        except (re.error, SyntaxError) as e:
            tb = traceback.extract_tb(e.__traceback__)
            line_number = tb[-1].lineno
            line_content = input_text.splitlines()[line_number - 1].strip()
            raise SyntaxError(f"Syntax Error in {filename} on line {line_number}: {e} near '{line_content}'") from None

    def _remove_comments(self, text):
        return re.sub(COMMENT_PATTERN, "", text, flags=re.DOTALL)

    def _process_constants(self, text):
        matches = re.findall(CONST_PATTERN, text)
        for name, value in matches:
            value = value.strip()
            if name in self.constants:
                raise SyntaxError(f"Duplicate constant definition: {name}")
            if re.match(NUMBER_PATTERN, value):
                self.constants[name] = int(value)
            elif re.match(STRING_PATTERN, value):
                self.constants[name] = re.sub(r'\\"', '"', value[1:-1])
            elif re.match(ARRAY_PATTERN, value):
                array_items_str = re.findall(ARRAY_PATTERN, value)[0]
                array_items = [item.strip() for item in re.split(r'\s*,\s*|\s+', array_items_str) if item]
                self.constants[name] = [self._parse_value(item) for item in array_items]
            else:
                raise SyntaxError(f"Invalid constant value: {value}")

    def _replace_constants(self, text):
        def replace(match):
            const_name = match.group(1)
            if const_name not in self.constants:
                raise SyntaxError(f"Undefined constant: {const_name}")
            value = self.constants[const_name]
            if isinstance(value, list):
                return str(value).replace("'", '"')
            elif isinstance(value, str):
                return '"' + value + '"'
            else:
                return str(value)
        return re.sub(CONST_REF_PATTERN, replace, text)

    def _process_structure(self, text, filename, existing_keys=None, max_recursion=100, recursion_level=0):
        if recursion_level > max_recursion:
            raise RecursionError(f"Maximum recursion depth exceeded in {filename}")

        if existing_keys is None:
            existing_keys = set()

        text = self._replace_constants(text)
        result = []

        key_value_matches = re.findall(KEY_VALUE_PATTERN, text)
        for key, value in key_value_matches:
            key = key.strip()
            if key not in existing_keys:
                value = self._parse_value(value.strip(), filename)
                result.append({key: value})
                existing_keys.add(key)

        nested_blocks = re.findall(DICT_PATTERN, text, flags=re.DOTALL)
        for nested_block in nested_blocks:
            nested_result = self._process_structure(nested_block, filename, existing_keys, max_recursion, recursion_level + 1)
            result.extend(nested_result)

        return result

    def _parse_value(self, value, filename):
        value = value.strip()
        if re.match(STRING_PATTERN, value):
            return re.sub(r'\\"', '"', value[1:-1])
        elif re.match(NUMBER_PATTERN, value):
            return int(value)
        elif re.match(ARRAY_PATTERN, value):
            array_items_str = re.findall(ARRAY_PATTERN, value)[0]
            array_items = [item.strip() for item in re.split(r'\s*,\s*|\s+', array_items_str) if item]
            return [self._parse_value(item, filename) for item in array_items]
        elif re.match(DICT_PATTERN, value, flags=re.DOTALL):
            return self._process_structure(value, filename)
        else:
            raise SyntaxError(f"Invalid value '{value}' in {filename}")



def main():
    if len(sys.argv) != 2:
        print("Usage: python config_parser.py <path_to_config>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            input_text = f.read()
        parser = ConfigParser()
        yaml_output = parser.parse(input_text, config_file)
        print(yaml_output)
    except FileNotFoundError:
        print(f"Error: File '{config_file}' not found.")
        sys.exit(1)
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc() #Print the traceback for debugging purposes.
        sys.exit(1)


if __name__ == "__main__":
    main()