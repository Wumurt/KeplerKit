def read_tle_file(path_tle):
    with open(path_tle) as f:
        lines = [line.strip() for line in f if line.strip()]
        print(f'файл {path_tle} открыт, считано {len(lines)} строк')

    tle_list = []
    for i in range(0, len(lines), 3):
        name = lines[i]
        line1 = lines[i + 1]
        line2 = lines[i + 2]
        tle_list.append((name, line1, line2))
    print(f'return to main {len(tle_list)} TLEs')
    return tle_list
