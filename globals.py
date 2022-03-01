def init_globals():
    global images_per_char
    global base
    global inter_delay
    images_per_char = 3
    base = 5
    inter_delay = 400

def dec_to_base(num, base):  #Maximum base - 36
    base_num = ""
    while num>0:
        dig = int(num%base)
        if dig<10:
            base_num += str(dig)
        else:
            base_num += chr(ord('A')+dig-10)  #Using uppercase letters
        num //= base

    base_num = base_num[::-1]  #To reverse the string
    return base_num
