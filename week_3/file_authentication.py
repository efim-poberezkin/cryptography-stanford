import os
from binascii import hexlify

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


TARGET_FILE = "week_3/6.1.intro.mp4_download"
TEST_FILE = "week_3/6.2.birthday.mp4_download"
TEST_HASH_ZERO_EXPECTED = (
    "03c08f4ee0b576fe319338139c045c89c3e8e9409633bea29442e21425006ea8"
)
BLOCK_SIZE = 1024


def main():
    test_hash_zero = compute_hash_zero(TEST_FILE, BLOCK_SIZE)
    assert test_hash_zero == TEST_HASH_ZERO_EXPECTED
    print(f"Test file hash zero: {test_hash_zero}")

    target_hash_zero = compute_hash_zero(TARGET_FILE, BLOCK_SIZE)
    print(f"Target file hash zero: {target_hash_zero}")


# Test file hash zero: 03c08f4ee0b576fe319338139c045c89c3e8e9409633bea29442e21425006ea8
# Target file hash zero: 5b96aece304a1422224f9a41b228416028f9ba26b0d1058f400200f06a589949


def compute_hash_zero(fname, block_size, hexlify_final_hash=True):
    block_hash = b""
    for block in read_blocks_in_reverse(fname, block_size):
        augmented_block = block + block_hash
        block_hash = hashes.Hash(hashes.SHA256(), backend=default_backend())
        block_hash.update(augmented_block)
        block_hash = block_hash.finalize()
    if hexlify_final_hash:
        block_hash = hexlify(block_hash).decode("ascii")
    return block_hash


def read_blocks_in_reverse(fname, block_size):
    fsize = os.path.getsize(fname)
    last_block_size = fsize % block_size
    with open(fname, "rb") as f:
        for pos in range(fsize - last_block_size, -1, -block_size):
            f.seek(pos)
            block = f.read(block_size)
            yield block


if __name__ == "__main__":
    main()
