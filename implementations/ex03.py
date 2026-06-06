import hashlib

VERSION = 2

PREVIOUS_BLOCK = (
    "00000000d1145790a8694403d4063f323d499e655c83426834d4ce2f8dd4a2ee"
)

MERKLE_ROOT = """c0a692de10b69e2381a2856dcb0d0736dcd307bf25af7ce74831bf25793de626
aad3a3466dc5343599afa34ef94e061418e4b161aa12ee4b93b713a9a3e75fc2
f0fa6a147eb785d3669f09a8aa295ec771a82cc7ea3300598f35b4b204661112
31e224f6d7afa0c5fffe78f77f202770dcb7c5aa21782ad02f933f7d601f0469
f4ae4682b220bcce026aadf1f228c78549edc8a126f7ce1352c4b45809ebbf96
7c8d5e7d0f2f70c936068c9707c39f551faeb0fecc15afc79bead483b5a661cc
e679dad8b0aa80768c147ee7e81ac0a6fa0a7fa458638ab8914979f7a1dd6f01
c8bff989b8b5db32ae7aac8ceed7fc1643aff1a9e451a994c0def372f542b663
6f9f7ee3b8e90bc802cc247c01d912032a9e064dff629eb534aa8b8060422467
14791f369f719187b0349c57b33f96eaf906caf1d4b51772c93027c440706c27
74bdcc88d6e08725214adb4399d76ffafe129257bb79a242270d180749819ef3
a647dce7934842454ea107c44f24dcf35e3e5e61a040f16b1a9e258cc4be49cc
4815c5c308541d57129f6e5274894e12206b0fd38f987268983afb608aa26ce4
"""

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
