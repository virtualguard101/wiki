from ruamel.yaml import YAML
from pathlib import Path


p = Path('docs/.nav.yml')
yaml = YAML()
yaml.preserve_quotes = True
yaml.width = 4096
yaml.indent(mapping=2, sequence=2, offset=2)
with p.open('r', encoding='utf-8') as f:
    data = yaml.load(f)
with p.open('w', encoding='utf-8') as f:
    yaml.dump(data, f)
