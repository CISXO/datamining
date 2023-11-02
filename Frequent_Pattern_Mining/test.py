from Cryptodome.Cipher import DES

key = b'-8B key-'
plaintext = b'Hello my name is Jo Jeong Hyeon '

# DES 암호화 객체 생성
cipher = DES.new(key, DES.MODE_OFB)

# 암호화
msg = cipher.iv + cipher.encrypt(plaintext)

# 암호화된 메시지를 복호화하기 위함
cipher = DES.new(key, DES.MODE_OFB, iv=msg[:8])

# 복호화
decrypted_message = cipher.decrypt(msg[8:])

print("평문: {}\n암호문: {}".format(plaintext, msg))
print("복호화된 메시지: {}".format(decrypted_message.decode('utf-8')))
