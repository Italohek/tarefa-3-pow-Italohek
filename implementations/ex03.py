import hashlib

VERSION = 2

PREVIOUS_BLOCK = (
    "00000000d1145790a8694403d4063f323d499e655c83426834d4ce2f8dd4a2ee"
)

MERKLE_ROOT = "ed33f4671f90013a6b9c8f03cc6336b97e65b2317ce6072381dc19ecc67e3bca"

MIN_TIMESTAMP = 1230999305

MAX_TIMESTAMP = 1231723825

TARGET = int(
    "00000000ffff0000000000000000000000000000000000000000000000000000",
    16
)


def create_header(version, prev_block, merkle_root, timestamp, nonce):

    version_hex = version.to_bytes(4, "big").hex()

    timestamp_hex = timestamp.to_bytes(4, "big").hex()

    nonce_hex = nonce.to_bytes(8, "big").hex()

    return (
        version_hex +
        prev_block +
        merkle_root +
        timestamp_hex +
        nonce_hex
    )


def mine_block():

    print("Mining started...")

    for timestamp in range(MIN_TIMESTAMP, MAX_TIMESTAMP + 1):

        nonce = 0

        while nonce < (2**64):

            header = create_header(
                VERSION,
                PREVIOUS_BLOCK,
                MERKLE_ROOT,
                timestamp,
                nonce
            )

            block_hash = hashlib.sha256(
                bytes.fromhex(header)
            ).hexdigest()

            if int(block_hash, 16) <= TARGET:
                with open(
                    "solutions/exercise03.txt",
                    "w"
                ) as file:
                    file.write(header)
                print(
                    "Saved to solutions/exercise03.txt"
                )
                return
            nonce += 1

    print("No valid block found.")


if __name__ == "__main__":
    mine_block()
