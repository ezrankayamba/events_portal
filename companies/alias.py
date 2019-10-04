from itertools import product
from .models import Company


def not_used(a):
    if Company.objects.filter(email=f'{a}@gmail.com').first():
        return False
    else:
        return True


def possibles(email):
    aliases = []
    id = email.split('@')[0]
    p1 = id.replace('.', '')
    count = len(list(p1))
    combs = [p for p in product(range(2), repeat=count - 1)]
    chars = list(p1)
    for cmb in combs:
        row = []
        for i, c in enumerate(chars):
            row.append(c)
            if i < len(chars) - 1 and cmb[i] == 1:
                row.append('.')
        a = (''.join(row))
        if a != id or not_used(a):
            aliases.append(a)
    return aliases


def get_alias(email):
    return next(iter(possibles(email)), None)
