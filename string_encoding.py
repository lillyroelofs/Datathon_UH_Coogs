
def string2binary(text):
    character_list = list(text)
    binary_list= []
    for character in character_list:
        char_bin =  bin(ord(character))[3:]
        binary_list.append(char_bin)
        #print(char_bin)
    return binary_list

stuff = string2binary("abcdefghijklmnopqrstuvwxyzA")

print(stuff[0])

#def binary2string(binary):