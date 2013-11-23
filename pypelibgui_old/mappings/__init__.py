import weather, timings, utils


modules = [weather, timings, utils]


def get_mappings():
    maps = {}
    for x in modules:
        for y in x.mappings:
            maps[y.__name__] = y
    return maps

