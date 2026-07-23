import socket, re

HOST, PORT = "38.47.176.164", 1006

# Integer value of b"Please give me the flag"
M = 7703033469609239351985350025414201079417630703156486503  # int.from_bytes(..., "big")

def recv_until(sock, needle):
    buf = b""
    while needle not in buf:
        chunk = sock.recv(8192)
        if not chunk:
            break
        buf += chunk
    return buf

with socket.create_connection((HOST, PORT)) as s:
    banner = recv_until(s, b"Please give me the flag")
    text = banner.decode()
    print(text)

    # Parse n and E(4) from the banner
    n = int(re.search(r"Public key \(n, g\) = \((\d+), \?\)", text).group(1))
    c4 = int(re.search(r"E\(4\) = (\d+)", text).group(1))
    s2 = n * n

    # Compute k = M * inv(4) mod n  (Python 3.8+: pow(4, -1, n) is the modular inverse)
    inv4 = pow(4, -1, n)
    k = (M * inv4) % n

    # Craft ciphertext: c = (E(4))^k mod n^2  == E(M)
    c = pow(c4, k, s2)

    # Send it
    s.sendall(str(c).encode() + b"\n")

    # Print the server's reply (should include the flag)
    try:
        while True:
            out = s.recv(4096)
            if not out:
                break
            print(out.decode(), end="")
    except Exception:
        pass
