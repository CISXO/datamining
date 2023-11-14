from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad, unpad

def generate_key():
    return get_random_bytes(16)  # 16 bytes key for AES-128

def encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
    return ciphertext, cipher.iv

def decrypt(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode('utf-8')

# 예제
if __name__ == "__main__":
    # 키 생성
    key = generate_key()

    # 암호화할 데이터
    data_to_encrypt = "Hello, AES encryption!"

    # 암호화
    encrypted_data, iv = encrypt(data_to_encrypt, key)
    print(f"Encrypted data: {encrypted_data.hex()}")

    # 복호화
    decrypted_data = decrypt(encrypted_data, key, iv)
    print(f"Decrypted data: {decrypted_data}")
