import requests


URL = "http://crypto-class.appspot.com/po?er="
TARGET_CT = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"
BLOCK_SIZE = 16  # bytes


def main():
    pt = decrypt_ct(TARGET_CT)
    pt_ascii = bytes.fromhex(pt).decode("ascii")
    print(f'ct decryption: "{pt_ascii}"')


def decrypt_ct(ct):
    ct_bytes = bytes.fromhex(ct)
    blocks = [ct_bytes[i : i + BLOCK_SIZE] for i in range(0, len(ct_bytes), BLOCK_SIZE)]

    pt = ""
    for i in range(1, len(blocks)):  # first block is IV so we skip decrypting it
        pt += decrypt_block(i, blocks).hex()

    return pt


def decrypt_block(block_num, blocks):
    print(f"decrypting block #{block_num}...")

    block = blocks[block_num]
    prev_block = blocks[block_num - 1]

    block_decryption = bytearray(BLOCK_SIZE)  # will be adjusted with guessed bytes by reference

    for byte_num in range(BLOCK_SIZE - 1, -1, -1):
        guess_and_save_byte(block, byte_num, prev_block, block_decryption)

    print(f"block #{block_num} decryption: {block_decryption.hex()}")
    print(f"block #{block_num} ascii: \"{block_decryption.decode('ascii')}\"")
    return block_decryption


def guess_and_save_byte(block, byte_num, prev_block, block_decryption):
    pad_byte = BLOCK_SIZE - byte_num
    pad = bytes([pad_byte] * BLOCK_SIZE)

    for g in range(256):
        block_decryption[byte_num] = g  # guessing block decryption
        ct_guess = bxor(prev_block, bxor(pad, block_decryption)) + block
        if query(ct_guess) is True:
            print(f"byte #{byte_num + 1}: {hex(g)}")
            return

    raise Exception("Unable to guess byte")


def query(ct_bytes):
    ct = ct_bytes.hex()
    r = requests.get(URL + ct)

    if r.status_code == 404:
        return True  # good padding
    elif r.status_code == 403:
        return False  # bad padding
    else:
        raise Exception(f"Got unexpected status code: {r.status_code}")


def bxor(bytes1, bytes2):
    return bytes([a ^ b for a, b in zip(bytes1, bytes2)])


if __name__ == "__main__":
    main()
