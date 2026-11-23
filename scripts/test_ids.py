import re

with open(r'C:\Users\julio\dev\sitio-web-csd\src\reserva-cupo.njk', encoding='utf-8') as f:
    content = f.read()

ids_used = re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", content)
ids_defined = set(re.findall(r"id=['\"]([^'\"]+)['\"]", content))

print('Total IDs usados en JS:', len(ids_used))
missing = [i for i in ids_used if i not in ids_defined]
print('IDs faltantes en HTML:', missing)
