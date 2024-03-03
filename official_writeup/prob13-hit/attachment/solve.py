import base64

def find_inverse(a):
    for x in range(256):
        if (a * x) % 256 == 1:
            print(x)
            return x
    return None

def inverse_linear(dst, a, B):

    inverse_a = find_inverse(a)
    if inverse_a is None:
        raise ValueError(f"No multiplicative inverse for {a} under mod 256")
    return [(inverse_a * (dst[i] - B[i])) % 256 for i in range(len(dst))]

# Assuming encrypted_password is your encrypted password
password = "%%xv$v^DlcLABnMaxNF^ndm*OXr^r$?v-AJoOJczCo$."
a = 0xE9
standard_base64_table = "asdfghjklqwertyuiopzxcvbnmQWERTYUIOPZXCVBNMASDFGHJKL$%^)!@#&*(-?."
translation_table = str.maketrans(standard_base64_table, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=")
password = [b for b in list(base64.b64decode(password.translate(translation_table)))]
B = [0x01, 0x09, 0xCD, 0x12, 0x7A, 0x9E, 0x79, 0xF1, 0x74, 0x19, 0x19, 0x0C, 0xDB, 0x6F, 0x25, 0x14, 0xDD, 0x61, 0x13, 0xE2, 0x8B, 0xBC, 0xC4, 0x26, 0x83, 0xBE, 0xB8, 0x70, 0xAA, 0x4A, 0x90, 0x58]

# Decrypt the password
password = inverse_linear(password, a, B)


for i in password:
    print(chr(i), end='')