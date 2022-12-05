
text = 'You'

def str_to_binary(str):
    ls = []
    for i in str:
        ls.append(bin(ord(i))[2:])

    for i in range(len(ls)):
        if len(ls[i]) < 8:
            n  = 8 -len(ls[i])
            ls[i] = n*'0' + ls[i]
    binary_str = ' '.join(ls)   
    return binary_str

def binary_to_int(str):
    return None


def check_str(str):
    lowerCase = str.lower()
    if str_to_binary(str) == "01111001 01101111 01110101":
        return "You got it"
    else:
        return "Wrong"


def test():
    assert str_to_binary("SOS") == "01010011 01001111 01010011"
    assert str_to_binary("hello") == "01101000 01100101 01101100 01101100 01101111"


def main():
    test()


if __name__ == "__main__":
    main()