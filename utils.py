def unary(q):
    code1 = []
    for i in range(q):
        code1.append(1)
    code1.append(0)
    code2 = [str(i) for i in code1]
    code = "".join(code2)
    return code


def rem_trun(r, k):
    rem = bin(r)
    return rem[2:].zfill(k)