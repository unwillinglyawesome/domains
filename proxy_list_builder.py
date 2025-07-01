from pathlib import Path

domains = []

src_dir = Path("proxy")
for filepath in src_dir.iterdir():
    if filepath.is_file():
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                domains.append(line.strip())

domains.sort()

with open('lists/proxy.lst', 'w', encoding='utf-8', newline='\n') as file:
    for domain in domains:
        file.write(f"nftset=/{domain}/4#inet#fw4#vpn_domains\n")
