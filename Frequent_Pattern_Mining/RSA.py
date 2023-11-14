from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

def generate_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt(plaintext, public_key):
    key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(key)
    ciphertext = cipher.encrypt(plaintext.encode('utf-8'))
    return ciphertext

def decrypt(ciphertext, private_key):
    key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(key)
    plaintext = cipher.decrypt(ciphertext).decode('utf-8')
    return plaintext

# 예제
if __name__ == "__main__":
    # 키 생성
    private_key, public_key = generate_key_pair()

    # 암호화할 데이터
    data_to_encrypt = "Hello, RSA encryption!"

    # 암호화
    encrypted_data = encrypt(data_to_encrypt, public_key)
    print(f"Encrypted data: {encrypted_data.hex()}")

    # 복호화
    decrypted_data = decrypt(encrypted_data, private_key)
    print(f"Decrypted data: {decrypted_data}")
