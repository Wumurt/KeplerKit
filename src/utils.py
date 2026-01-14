from pathlib import Path
from datetime import datetime


def get_output_dir(
        base_dir: str = 'data',
        date_format: str = '%Y-%m-%d',
        nested: bool = True
) -> Path:
    """
    Возвращает путь вида base_dir/YYYY-MM-DD и гарантирует,
    что каталог существует.

    nested=True -> data/YYYY/MM/YYYY-MM-DD
    nested=False -> data/YYYY-MM-DD

    """
    local_time = datetime.now()
    date_str = local_time.strftime(date_format)

    if nested:
        year = local_time.strftime('%Y')
        month = local_time.strftime('%m')
        output_dir = Path(base_dir) / year / month / date_str
    else:
        output_dir = Path(base_dir) / date_str

    output_dir.mkdir(parents=True, exist_ok=True)
    print(f'[INFO] The {output_dir} directory was successfully created.')

    return output_dir
