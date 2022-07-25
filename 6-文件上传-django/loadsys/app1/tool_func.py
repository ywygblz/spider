# AES加密
from Crypto.Cipher import AES

key = '1234567812345678'  # 秘钥
password_key = key.encode()
aes = AES.new(password_key, AES.MODE_ECB)

var_line = 0


# 补位
def add_16(text: bytes):
    global var_line
    var_line = len(text)
    add_long = 16 - len(text) % 16
    if add_long == 16:
        return text
    result = text + b'\0' * add_long
    # print(result, len(result))
    return result


# 删除补位
def del_empty(b_text: bytes):
    return b_text[:var_line]


# 加密
def b_encrypt(b_text: bytes):
    b_text = add_16(b_text)
    return aes.encrypt(b_text)


# 解密
def b_decrypt(b_text: bytes):
    result = del_empty(aes.decrypt(b_text))
    return result



