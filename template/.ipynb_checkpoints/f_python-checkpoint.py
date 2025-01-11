def invert_dict(d):
    inverted = {}
    for key, value in d.items():
        if value not in inverted:
            inverted[value] = key
        else:
            inverted[value].append(key)
    return inverted