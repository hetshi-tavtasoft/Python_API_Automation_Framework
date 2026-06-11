def merge_dicts(base, override):
    result = base.copy()
    result.update(override)
    return result


def truncate(text, max_length=1000):
    return text[:max_length] if text and len(text) > max_length else text
