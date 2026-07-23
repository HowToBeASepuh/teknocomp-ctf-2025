import os

from Crypto.Util.number import bytes_to_long, getPrime

flag = os.getenvb(b"FLAG", b"Teknocom{UUUUUUFAKEFLAGGGGG}")
assert flag.startswith(b"Teknocom{")
m = bytes_to_long(flag)
e = 0x10001
p = getPrime(1024)
q = getPrime(1024)
n = p * q
e = 65537
phi = (p-1)*(q-1)
d = pow(e, -1, phi)
hint = p+q
c = pow(m,e,n)

print(f"e={e}")
print(f"d={d}")
print(f"hint={hint}")
print(f"c={c}")
