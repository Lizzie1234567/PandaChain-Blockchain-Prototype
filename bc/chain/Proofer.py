import hashlib

import bc.chain.Block as Block

# the upper bound of all potential nonce
MAX_NONCE = 2 ** 32


def verify_proof(block: Block) -> bool:
    """
    Verifying if the Proof-of-Work is correct, based on a specific difficulty.
    :param block:The BLock on the blockchain
    :return: Whether the Proof-of-Work found is valid or not.
    """

    if block.dynamic_difficulty <= 0:
        raise ValueError("Difficulty must be a positive number!")

    return block.current_block_hash[:block.dynamic_difficulty] == "0" * block.dynamic_difficulty


def proof_of_work(block: Block) -> int:
    """
    Proof-of-Work algorithm. Increment a random number and trying to verify it
    each time until Proof-of-work returns True.
    :param block:The BLock on the blockchain
    :return:
    """

    # calculate the difficulty target from difficulty bits
    target = 2 ** (256 - block.dynamic_difficulty)

    # perform the iteration, until finding a nonce which satisfies the target
    for nonce in range(MAX_NONCE):
        hash_res = hashlib.sha256(
            (str(str(block.height) +
                 str(block.previous_block_hash) +
                 str(block.timestamp) + str(block.dynamic_difficulty) +
                 str(nonce) + str(block.merkle_tree_root)).encode('utf-8')))
        if int(str(hash_res), 16) < target:  # difficult requirement
            print(f'success with nonce {nonce}\n')
            print(f'hash is:\t\t {hash_res}')
            return nonce

    # target cannot be satisfied even all nonce are traversed
    print(f'failed after {MAX_NONCE} tries\n')
    return MAX_NONCE
