import hashlib

chars = "                                        P3*UmMZ}'by+4K7/9jwSOi2A&$İdı\\_ICYEDN.fhHQzlT![?xtV]@-=<krJ0+g65eaG#L{-pBğunü`%8R|cqsv>oX,~WF1"


def find(str, ch):
    for i, ltr in enumerate(str):
        if ltr == ch:
            yield i


def encode(yazi):
    uzunluk = len(yazi)
    i = 0
    p = 1
    dizi = []
    while i < uzunluk:
        try:
            e = list(find(f"{chars}", f"{yazi[i]}"))
            if len(str(e)) == 4:
                kacinci = str(e)[1:3]
                dizi.append(((int(kacinci) + 4) * 257 + 29) * 2 + (p * 7))
            elif len(str(e)) == 3:
                kacinci = str(e)[1:2]
                dizi.append(((int(kacinci) + 4) * 257 + 29) * 2 + (p * 7))
            else:
                kacinci = str(e)[1:4]
                dizi.append(((int(kacinci) + 4) * 257 + 29) * 2 + (p * 7))
            i += 1
            p += 1
        except IndexError:
            pass

    hash_sifre = "".join(list(map(str, dizi)))
    for i in range(12954):
        hash_sifre = hashlib.sha3_512(hash_sifre.encode()).hexdigest()

    return hash_sifre