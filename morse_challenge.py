import winsound
from time import sleep


def str_to_morse(word):
    """Converts a string into a morse string"""

    # File that contains mapping between morse code and characters
    mapping_path = "resources/morse_mapping.txt"

    # Creates a dictionary that maps morse code and characters
    with open(mapping_path, 'r') as infile:
        mapping = dict()
        for line in infile:
            string, morse = line[:-1].split('\t')
            mapping.update({string: morse})

    # Creates a list of words within input string
    word_list = list(word.upper().strip())
    output_list = []

    for char in word_list:
        if char.isspace():
            output_list.pop()
            output_list.append('/')
        elif char not in mapping:
            return None
        else:
            output_list.append(mapping[str(char)])
            output_list.append(" ")
    
    return str(''.join(output_list))


def morse_audio(morse_str):
    """Translates a morse string into audio"""

    # Define frequency (frq) and duration of each beep (base_dur)
    frq = 500
    base_dur = 100
    
    # short mark, dot or dit: "dit duration" is one time unit long
    # long mark, dash or dah: three time units long
    # inter-element gap between the dits and dahs within a character: one dot duration or one unit long
    # short gap (between letters): three time units long
    # medium gap (between words): seven time units long

    for char in morse_str:
        if char == '.':
            winsound.Beep(frq, base_dur)
        elif char == '-':
            winsound.Beep(frq, base_dur * 3)
        elif char == "/":
            sleep(base_dur / 1000 * 7)
            continue
        elif char.isspace():
            sleep(base_dur / 1000 * 3)
            continue
        sleep(base_dur / 1000)


def test():
    assert str_to_morse("SOS") == "... --- ... "
    assert str_to_morse("testing 123") == "- . ... - .. -. --./.---- ..--- ...-- "
    assert str_to_morse("SOS?!") == "... --- ... ..--.. -.-.-- "
    assert str_to_morse("パイソンは好きです") == None


def main():
    test()
    morse_audio(str_to_morse("SOS"))


if __name__ == "__main__":
    main()