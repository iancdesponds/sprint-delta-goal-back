import hashlib

try:
    result = hashlib.scrypt(b"test password", salt=b"salt", n=16384, r=8, p=1)
    print("hashlib.scrypt está disponível.")
    print("Resultado do hash:", result)
except AttributeError as e:
    print("hashlib.scrypt não está disponível: ", e)
