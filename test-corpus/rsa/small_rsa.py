from Crypto.Util.number import bytes_to_long, getPrime

p, q = getPrime(512), getPrime(512)
n, e = p * q, 3
m = bytes_to_long(b'CTF_RSA_SMOKE_TEST')
c = pow(m, e, n)
print(f'n={n}\ne={e}\nc={c}')
