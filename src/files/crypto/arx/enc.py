#!/usr/bin/env python3

class baby_arx():
    def __init__(self, key):
        assert len(key) == 64, f"Key length must be 64 bytes, got {len(key)}"
        self.state = list(key)

    def b(self):
        b1 = self.state[0]
        b2 = self.state[1]
        b1 = (b1 ^ ((b1 << 1) | (b1 & 1))) & 0xff
        b2 = (b2 ^ ((b2 >> 5) | (b2 << 3))) & 0xff
        b = (b1 + b2) % 256
        self.state = self.state[1:] + [b]
        return b

    def stream(self, n):
        return bytes([self.b() for _ in range(n)])


FLAG = open('./flag.txt', 'rb').read().strip()

if len(FLAG) < 64:
    FLAG += b'0' * (64 - len(FLAG))  
elif len(FLAG) > 64:
    FLAG = FLAG[:64] 

cipher = baby_arx(FLAG)
out = cipher.stream(64).hex()
print(out)
