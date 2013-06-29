from unicodedata import normalize as ucnorm, category


def normalize(text):
    if not isinstance(text, unicode):
        text = unicode(text)
    text = text.lower()
    decomposed = ucnorm('NFKD', text)
    filtered = []
    for char in decomposed:
        cat = category(char)
        if char == "'":
            continue
        if cat.startswith('C'):
            filtered.append(' ')
        elif cat.startswith('M'):
            # marks, such as umlauts
            continue
        elif cat.startswith('Z'):
            # newlines, non-breaking etc.
            filtered.append(' ')
        elif cat.startswith('S'):
            # symbols, such as currency
            continue
        elif cat.startswith('L') or cat.startswith('N'):
            filtered.append(char)
        else:
        #    print (cat, char)
            filtered.append(' ')
    text = u''.join(filtered)
    while '  ' in text:
        text = text.replace('  ', ' ')
    text = text.strip()
    return ucnorm('NFKC', text)
