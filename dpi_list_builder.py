from pathlib import Path


def make_dpi_list() -> None:
    domains = []
    src_dir = Path("dpi")
    for filepath in src_dir.iterdir():
        if filepath.is_file():
            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    if line.strip():
                        domains.append(line.strip())

    domains.sort()

    with open('lists/zapret.lst', 'w', encoding='utf-8', newline='\n') as file:
        for domain in domains:
            file.write(domain + '\n')
