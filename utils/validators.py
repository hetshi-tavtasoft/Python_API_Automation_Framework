def has_keys(data, *keys):
    return all(key in data for key in keys)


def is_valid_email(email):
    return isinstance(email, str) and "@" in email
