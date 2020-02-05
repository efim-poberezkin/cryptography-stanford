import os
from binascii import hexlify

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


TARGET_FILE = "week_3/6.1.intro.mp4_download"
TEST_FILE = "week_3/6.2.birthday.mp4_download"
TEST_HASH_ZERO_EXPECTED = "03c08f4ee0b576fe319338139c045c89c3e8e9409633bea29442e21425006ea8"
BLOCK_SIZE = 1024


def main():
    for file in [TEST_FILE, TARGET_FILE]:
        print(f"--- File: {file} ---")

        # compute hash zero and save augmented file
        augmented_file = "week_3/augmented.bin"
        hash_zero = compute_hash_zero(file, BLOCK_SIZE, augmented_file)
        hash_zero_hex = hexlify(hash_zero).decode("ascii")
        if file == TEST_FILE:
            assert hash_zero_hex == TEST_HASH_ZERO_EXPECTED
        print(f"Hash zero: {hash_zero_hex}")

        # verify saved augmented file with computed hash
        verification_res = verify_augmented_file(augmented_file, BLOCK_SIZE, hash_zero)
        print(f"Passes verification with computed hash zero: {verification_res}")


# --- File: week_3/6.2.birthday.mp4_download ---
# Hash zero: 03c08f4ee0b576fe319338139c045c89c3e8e9409633bea29442e21425006ea8
# Passes verification with computed hash zero: True
# --- File: week_3/6.1.intro.mp4_download ---
# Hash zero: 5b96aece304a1422224f9a41b228416028f9ba26b0d1058f400200f06a589949
# Passes verification with computed hash zero: True


def compute_hash_zero(fname, block_size, augmented_file_path=None):
    block_hash = b""
    augmented_blocks = []
    for block in read_blocks_in_reverse(fname, block_size):
        augmented_block = block + block_hash
        augmented_blocks.insert(0, augmented_block)
        block_hash = hash_block(augmented_block)
    if augmented_file_path is not None:
        with open(augmented_file_path, "wb") as f:
            for block in augmented_blocks:
                f.write(block)
    return block_hash


def read_blocks_in_reverse(fname, block_size):
    fsize = os.path.getsize(fname)
    last_block_size = fsize % block_size
    with open(fname, "rb") as f:
        for pos in range(fsize - last_block_size, -1, -block_size):
            f.seek(pos)
            block = f.read(block_size)
            yield block


def verify_augmented_file(augmented_file, block_size, hash_zero):
    hash_size = 32
    res = True
    augmented_block_size = block_size + hash_size
    expected_hash = hash_zero
    for block in read_blocks(augmented_file, augmented_block_size):
        block_hash = hash_block(block)
        if block_hash != expected_hash:
            res = False
            break
        expected_hash = block[-hash_size:]
    return res


def read_blocks(fname, block_size):
    fsize = os.path.getsize(fname)
    with open(fname, "rb") as f:
        while True:
            block = f.read(block_size)
            if block:
                yield block
            else:
                # the block is empty, which means we're at the end of the file
                return


def hash_block(block):
    block_hash = hashes.Hash(hashes.SHA256(), backend=default_backend())
    block_hash.update(block)
    block_hash = block_hash.finalize()
    return block_hash


if __name__ == "__main__":
    main()
