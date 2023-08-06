import os
import traceback
import sys
import ctypes


def to_boolean(value):
    return str(value).lower() == "true"


def to_int32(value):
    return ctypes.c_int(int(value)).value


_defaultValues = {
    "enable_sql_trace": True,
    "ignore_url_postfix": [".css", ".js", ".ico"],
    "max_number_of_method": 30000,
    "max_number_of_text": 20000,
    "max_number_of_sql": 10000,
    "max_number_of_stack": 30000,
    "dump_http_query": True,
    "enable_http_only_for_wmonid_cookie": False,
    "enable_secure_for_wmonid_cookie": False,
    "expire_date_for_wmonid_cookie": 365,
    "guid_max_length": -1,
    "enable_guid_from_txid": False,
    "guid_http_header_key": "_J_GUID_",
    "redis_as_external_call": False,
    "topology_http_header_key": "X-J_HTTP_TUID_",
    "topology_mode": True,
    "profile_http_header_all": False,
    "profile_http_header": None,
    "profile_http_value_length": 40,
    "enable_multi_tier_trace": True,
    "profile_http_parameter": None,
    "min_sql_time_to_collect": 0,
    "min_sql_time_to_collect_parameter": 0,
    "remote_address_header_key": None,
    "remote_address_header_key_delimiter": ",",
    "remote_address_header_key_idx": 0,
}

_valueFunc = {
    "enable_sql_trace": to_boolean,
    "max_number_of_method": to_int32,
    "max_number_of_text": to_int32,
    "max_number_of_sql": to_int32,
    "max_number_of_stack": to_int32,
    "dump_http_query": to_boolean,
    "enable_http_only_for_wmonid_cookie": to_boolean,
    "enable_secure_for_wmonid_cookie": to_boolean,
    "expire_date_for_wmonid_cookie": to_int32,
    "guid_max_length": to_int32,
    "enable_guid_from_txid": to_boolean,
    "redis_as_external_call": to_boolean,
    "topology_mode": to_boolean,
    "profile_http_header_all": to_boolean,
    "profile_http_value_length": to_int32,
    "enable_multi_tier_trace": to_boolean,
    "min_sql_time_to_collect": to_int32,
    "min_sql_time_to_collect_parameter": to_int32,
    "remote_address_header_key_idx": to_int32,
}


class AppConfig(object):
    def __init__(self, config_path):
        self.path = None
        self.config = None
        self.cache = {}
        self._load_config(config_path)

    def get_attr_by_name(self, attr_name):
        return self.__getattr__(attr_name)

    def __getattr__(self, attr_name):
        cached_value = self.cache.get(attr_name)
        if cached_value is not None:
            return cached_value

        if self.config is None:
            return None

        try:
            value_func = _valueFunc.get(attr_name)
            default_value = _defaultValues.get(attr_name)

            if not self.config.has_option('JENNIFER', attr_name):
                attr_value = self.config.get('SERVER', attr_name, default_value)
            else:
                attr_value = self.config.get('JENNIFER', attr_name, default_value)

            if attr_value is None:
                return None

            if value_func is None:
                self.cache[attr_name] = attr_value
                return attr_value

            result = value_func(attr_value)
            self.cache[attr_name] = result

            return result
        except:
            return None

    def reload(self):
        self._load_config(self.path)

    def _load_config(self, config_path):
        from jennifer.agent import config_parser

        if config_path is None:
            return

        print_out = sys.stdout
        if sys.stdout.closed:
            print_out = sys.stderr

        try:
            self.path = config_path
            self.config = config_parser.ConfigParser()

            if len(self.cache) != 0:
                msg = str(os.getpid()) + ' jennifer ' + 'config_changed' + os.linesep
                print_out.write(msg)

            self.cache = {}
            self.config.read(config_path)
        except Exception as e:
            msg = str(os.getpid()) + ' jennifer.exception ' + 'load_config ' + config_path + ' ' + str(e) + os.linesep
            print_out.write(msg)
            traceback.print_exc()
