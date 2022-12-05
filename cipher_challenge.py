# we are importing string library
import string
#Code to add widgets will go here

plain_text="Look"
shift=8
alpha=[string.ascii_lowercase,string.ascii_uppercase,string.punctuation]
# this is a function for the caesar 
def caesar(text,shift,alphabets):
    def shift_alphabet(alphabets):
        return alphabets[shift:]+alphabets[:shift]

    shifted_alphabets=tuple(map(shift_alphabet,alphabets))
    final_alphabet=''.join(alphabets)
    final_shifted_alphabet=''.join(shifted_alphabets)
    table=str.maketrans(final_alphabet,final_shifted_alphabet)
    return text.translate(table)

def test():
    assert caesar(plain_text,shift,alpha) == "Twws"


def main():
    test()

if __name__ == "__main__":
    main()