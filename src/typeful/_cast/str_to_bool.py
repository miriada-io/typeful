def str_to_bool(bool_str: str) -> bool:
    true_values = {"true", "1", "on", "+", "yes"}
    false_values = {"false", "0", "off", "-", "no"}
    lowed_str = bool_str.lower()
    if lowed_str in true_values:
        return True
    if lowed_str in false_values:
        return False
    raise ValueError(f'invalid literal for boolean: "{lowed_str}"({type(lowed_str)})')
