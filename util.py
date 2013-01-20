def safe_float(s, range, default=False):
    try:
        f = float(s)
    except:
        return default

    if f > range[1]:
        return default
    if f < range[0]:
        return default

    return f
