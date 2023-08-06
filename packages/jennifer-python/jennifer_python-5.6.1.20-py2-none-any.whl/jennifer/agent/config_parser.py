
import os


class ConfigParser(object):
    def __init__(self):
        self.sections = {}
        self.config_path = None

    def read(self, config_path):
        self.config_path = config_path

        with open(config_path, 'r') as config_file:
            current_section = ''

            for line in config_file.readlines():
                line = ConfigParser.remove_comment(line)

                section_name, is_section = ConfigParser.get_section(line, current_section)
                if is_section:
                    current_section = section_name

                if current_section == '':
                    continue

                items = line.split('=')
                if len(items) != 2:
                    continue

                key = items[0].strip(' ')
                value = items[1].strip(' ')

                key_value = self.make_key_value(current_section, key, value)

                if current_section not in self.sections:
                    self.sections[current_section] = {}

                section_dict = self.sections[current_section]
                section_dict[key] = key_value

        return None

    def has_option(self, section_name, attr_name):
        section = self.sections.get(section_name)
        if section is None:
            return False

        item = section.get(attr_name)
        if item is None:
            return False

        return True

    @staticmethod
    def get_section(line, default_section):
        if len(line) < 3:
            return default_section, False

        if line[0] != '[':
            return default_section, False

        if line[len(line) - 1] != ']':
            return default_section, False

        return line[1:len(line) - 1], True

    def make_key_value(self, section_name, key, value):
        section = self.sections.get(section_name)
        if section is None:
            return value

        old_value = None
        try:
            if key == 'ignore_url_postfix' or key == 'profile_http_header'\
                    or key == 'profile_http_parameter':  # multiple values
                old_value = section.get(key)
                if old_value is None:
                    old_value = [value]
                else:
                    if isinstance(old_value, str):
                        old_value = [old_value, value]
                    elif isinstance(old_value, list):
                        old_value.append(value)
                    else:
                        print(os.getpid(), 'jennifer.exception', 'value type not supported', old_value, type(old_value))
                        old_value = None

                return old_value
        except Exception as e:
            print(os.getpid(), 'jennifer.exception', 'make_key_value', section_name, key, value, old_value, e)
            raise

        return value

    def get(self, section_name, key_name, default_value):
        section = self.sections.get(section_name)
        if section is None:
            return default_value

        key_value = section.get(key_name)
        if key_value is None:
            return default_value

        return key_value

    @staticmethod
    def remove_comment(line):
        return line.split('#')[0].strip(' ').strip()
