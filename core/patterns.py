COMMON_ERRORS = {
    'list_index_error': {
        'example': 'my_list[10] when my_list has only 3 items',
        'solution': 'Check list length: if len(my_list) > index:',
        'teaching_point': 'Lists are 0-indexed. Length 3 means indices 0, 1, 2 are valid.'
    },
    'dict_key_error': {
        'example': 'my_dict["key"] when "key" doesn\'t exist',
        'solution': 'Use my_dict.get("key") or check: if "key" in my_dict:',
        'teaching_point': 'Dictionaries throw KeyError for missing keys. .get() returns None instead.'
    },
    'none_attribute_error': {
        'example': 'result.method() when result is None',
        'solution': 'Check for None: if result is not None:',
        'teaching_point': 'Functions might return None. Always validate return values.'
    }
}