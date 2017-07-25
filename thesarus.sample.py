





thesarus = []


seq1 = []

seq2 = []

seq3 = ['312']


def build_thesarus(source):
    res = []
    for text in source:
        true_text = text.strip()
        if true_text != '':
            res.append(true_text)
    return res

thesarus = build_thesarus(seq1 + seq2 + seq3)

print(thesarus)