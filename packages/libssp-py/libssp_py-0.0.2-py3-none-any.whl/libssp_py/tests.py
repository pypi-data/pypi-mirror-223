import hashlib
from libssp_py.util import PASSWORD_CONSTANT, PASSWORD_HASHED_CONSTANT, PASSWORD_HASHED_HASHED_CONSTANT, generate_token, password_for_wifi, swap_endianness


def test_wifi():
    assert password_for_wifi('IPMANS-30276') == 'wlm26379'
    assert password_for_wifi('IPMANS-30238') == 'wlm26320'


def test_password_hash():
    sha1 = hashlib.sha1()
    sha1.update(PASSWORD_CONSTANT)
    hashed_passwd = sha1.digest()
    hashed_passwd_le = swap_endianness(hashed_passwd)
    assert hashed_passwd_le == PASSWORD_HASHED_CONSTANT

    sha1 = hashlib.sha1()
    sha1.update(hashed_passwd_le)
    hashed_hashed_passwd = sha1.digest()
    hashed_hashed_passwd_le = swap_endianness(hashed_hashed_passwd)
    assert hashed_hashed_passwd_le == PASSWORD_HASHED_HASHED_CONSTANT


def test_generate_token():
    challenge = bytes.fromhex("958bd664ca41bf0bd8a5c51341d61466f242492c")
    response = generate_token(challenge)
    assert response == bytes.fromhex("1f8d07e831452261576369273819186b345e4b4b")

if __name__ == '__main__':
    # TODO: real unit tests
    test_wifi()
    test_password_hash()
    test_generate_token()
    print("Tests passed")
