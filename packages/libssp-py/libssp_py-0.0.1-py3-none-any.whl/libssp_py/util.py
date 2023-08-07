import hashlib


def swap_endianness(b: bytes) -> bytes:
    """in pairs of 4, reverse the order of the bytes"""
    out = b''
    for i in range(0, len(b), 4):
        out += b[i:i+4][::-1]
    return out


def password_for_wifi(ssid: str) -> str:
    serial = ssid.split('-')[1]
    pwd = "wlm"
    passwd_array = ['6', '8', '3', '2', '4', '5', '9', '7', '0', '1']
    for n in serial:
        pwd += passwd_array[int(n)]
    return pwd


# See test.py: test_password_hash
PASSWORD_CONSTANT = b"zcam-live-password"
PASSWORD_HASHED_CONSTANT = bytes.fromhex("41677f4a2155c60561ede4a16842d01ad10e73f5")
PASSWORD_HASHED_HASHED_CONSTANT = bytes.fromhex("0dc527598982f95b581e6164d3e37b6569521eef")


def generate_token(challenge: bytes):
    sha1 = hashlib.sha1()

    sha1.update(challenge)
    sha1.update(PASSWORD_HASHED_HASHED_CONSTANT)

    hashed_hashed_passwd2 = sha1.digest()
    hashed_hashed_passwd2_le = swap_endianness(hashed_hashed_passwd2)

    # token = hashed_passwd XOR hashed_hashed_passwd:
    token = bytes([a ^ b for a, b in zip(PASSWORD_HASHED_CONSTANT, hashed_hashed_passwd2_le)])

    return token