def encode(text, shift):
    '''Moves text by shift number of moves, 
    Input = text is string, shift is integer'''

    encoded_text = ""

    for char in text:
        if char.isalpha():
            if char.isupper():
                base = 65
            else:
                base = 97
        
            index = ord(char) - base 
            shifted = index + shift
            wrapped = shifted % 26
            new_char = chr(wrapped + base)
            encoded_text += new_char
            # encoded_text += chr(((ord(char) - base) + shift ) % 26)
        else:
            encoded_text += char

    return encoded_text

def decode(text,shift):
    return encode(text, -shift)

print(encode("This is an example of a coded message.", 2))
print(decode("Vjku ku cp gzcorng qh c eqfgf oguucig.", 2))
