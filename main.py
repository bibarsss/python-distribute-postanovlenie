import os
from pathlib import Path
import sys
from pypdf import PdfReader

def read(file_path: str)->str:
    reader = PdfReader(file_path)

    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

    return full_text

def unique_target(save_dir: Path, file_path: Path) -> Path:
    target = save_dir / file_path.name
    counter = 1

    while target.exists():
        target = save_dir / f"{file_path.stem}_{counter}{file_path.suffix}"
        counter += 1

    return target

if getattr(sys, "frozen", False):
    base_path = Path(sys.executable).parent
else:
    base_path = Path(__file__).parent

legal = base_path / 'LEGAL'
legal.mkdir(exist_ok=True)

nova = base_path / 'CreditNOVA'
nova.mkdir(exist_ok=True)

for file_path in base_path.glob("*.pdf"):
    text = " ".join(read(str(file_path)).splitlines())

    if 'ПОСТАНОВЛЕНИЕ' not in text:
        continue

    print(file_path.name)

    if 'CreditNOVA' in text:
        target = unique_target(nova, file_path)
        file_path.replace(target)

    elif 'LEGAL' in text:
        target = unique_target(legal, file_path)
        file_path.replace(target)

print('Готово!')
