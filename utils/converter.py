import textwrap

c2n_dict = {
    "0"	: "ATA",
    "1"	: "TCT",
    "2"	: "GCG",
    "3"	: "GTG",
    "4"	: "AGA",
    "5"	: "CGC",
    "6"	: "ATT",
    "7"	: "ACC",
    "8"	: "AGG",
    "9"	: "CAA",
    "start"	: "TTG",
    "stop"	: "TAA",
    "A"	: "ACT",
    "B"	: "CAT",
    "C"	: "TCA",
    "D"	: "TAC",
    "E"	: "CTA",
    "F"	: "GCT",
    "G"	: "GTC",
    "H"	: "CGT",
    "I"	: "CTG",
    "J"	: "TGC",
    "K"	: "TCG",
    "L"	: "ATC",
    "M"	: "ACA",
    "N"	: "CTC",
    "O"	: "TGT",
    "P"	: "GAG",
    "Q"	: "TAT",
    "R"	: "CAC",
    "S"	: "TGA",
    "T"	: "TAG",
    "U"	: "GAT",
    "V"	: "GTA",
    "W"	: "ATG",
    "X"	: "AGT",
    "Y"	: "GAC",
    "Z"	: "GCA",
    "," : "AGC",
    "."	: "ACG",
}

n2c_dict = {
    "ATA": "0",
    "TCT": "1",
    "GCG": "2",
    "GTG": "3",
    "AGA": "4",
    "CGC": "5",
    "ATT": "6",
    "ACC": "7",
    "AGG": "8",
    "CAA": "9",
    "TTG": "start",
    "TAA": "stop",
    "ACT": "A",
    "CAT": "B",
    "TCA": "C",
    "TAC": "D",
    "CTA": "E",
    "GCT": "F",
    "GTC": "G",
    "CGT": "H",
    "CTG": "I",
    "TGC": "J",
    "TCG": "K",
    "ATC": "L",
    "ACA": "M",
    "CTC": "N",
    "TGT": "O",
    "GAG": "P",
    "TAT": "Q",
    "CAC": "R",
    "TGA": "S",
    "TAG": "T",
    "GAT": "U",
    "GTA": "V",
    "ATG": "W",
    "AGT": "X",
    "GAC": "Y",
    "GCA": "Z",
    "AGC":  "," ,
    "ACG":  "."	,
}

def str2ncs(st):
    ncs = ""
    for c in st.upper():
        if c in c2n_dict:
                ncs += c2n_dict[c]
        else:
            ncs += '_'
    return ncs

def ncs2str(ncs):
    ncs = textwrap.wrap(ncs.upper(), 3)
    st = ""
    for nc in ncs:
        if nc in n2c_dict:
            st += n2c_dict[nc]
        else:
            st += '_'
    return st