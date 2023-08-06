import base64


def truncate_value(value, max_length):
    if len(value) > max_length:
        return value[:max_length] + '...'

    return value[:max_length]


def encode_base64_cookie(data):
    return base64.b64encode(data).decode('ascii').replace('=', '%3D')


def decode_base64_cookie(data):
    return base64.b64decode(data.replace('%3D', '='))


def profile_http_parameter_message(o, dict_instance, param_list, header_value_length):
    text = []

    for param_key in param_list:
        param_value = dict_instance.get(param_key)
        if param_value is None:
            continue

        if isinstance(param_value, list):
            text.append(param_key + '=' + truncate_value(','.join(param_value), header_value_length))
        elif isinstance(param_value, str):
            text.append(param_key + '=' + truncate_value(param_value, header_value_length))

    if len(text) != 0:
        o.profiler.add_message('HTTP-PARAM: ' + '; '.join(text))
