import random

nucleotides = ['A', 'T', 'G', 'C']
error_types = ['_substitute', '_insert', '_delete']
error_types_prob = [0.5, 0.25, 0.25]


def decision(probability):
    return random.random() < probability

def decision_error_type():
    return random.choices(error_types, weights=error_types_prob)[0]

def errors_add(data, percent_error, k=30):
    datas = []
    while k > 0:
        d = ""
        for nuc in data:
            assert nuc in nucleotides, nuc + ' not in ' + str(nucleotides) + ' - ' + data
            if decision(percent_error):
                d += globals()[decision_error_type()](nuc)
            else:
                d += nuc
        datas.append(d)
        k -= 1
    return datas

def _substitute(c):
    nucs = nucleotides.copy()
    nucs.remove(c)
    return random.choice(nucs)

def _insert(c):
    if random.random() < 0.5:
        return c + random.choice(nucleotides)
    return random.choice(nucleotides) + c

def _delete(c):
    return ''