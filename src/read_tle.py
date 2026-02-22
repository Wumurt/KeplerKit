import logging

logger = logging.getLogger(__name__)


def read_tle_file(path_tle):
    with open(path_tle) as f:
        lines = [line.strip() for line in f if line.strip()]
        logger.info('файл %s открыт, считано %d строк', path_tle, len(lines))

    tle_list = []
    for i in range(0, len(lines), 3):
        name = lines[i]
        line1 = lines[i + 1]
        line2 = lines[i + 2]
        tle_list.append((name, line1, line2))
    logger.info('return to main %d TLEs', len(tle_list))
    return tle_list
