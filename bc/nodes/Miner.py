import threading

import bc.transactions as Transactions
import bc.chain as Chain
import bc.messages as Messages
import bc.network as Network

from . import ENodeType

from .Client import Client

from bc import log
from typing import Dict, List, Optional
from Crypto.PublicKey.RSA import RsaKey

from ..transactions import Transaction


class Miner(Client):
    verified_transactions: dict[str, Transaction]

    def __init__(self, private_key: RsaKey):
        super().__init__(private_key=private_key)

        # Store Verified transactions to input in the next block
        self.verified_transactions: Dict[str, Transactions.Transaction] = dict()

        # Settings
        self.__is_mining: bool = False
        self.__mining_thread = threading.Thread(target=self.__mine, daemon=True)

        # Construct Genesis Block on empty Blockchain
        if self.blockchain.size == 0:
            self._construct_genesis_block()

    @property
    def node_type(self) -> int:
        return ENodeType.MINER

    def refresh_balance(self):
        for my_utxo in self.my_UTXOs:
            my_utxo.get_balance(blockchain=self.blockchain)

    def _construct_genesis_block(self):
        self.construct_block(
            proof=42,
            previous_hash="first block"
        )

    def construct_block(self,
                        verified_transactions: List[Transactions.Transaction] = None,
                        proof=None,
                        previous_hash=None) -> Chain.Block:

        last_block: Chain.Block = self.blockchain.last_block
        dynamic_difficulty: int = 1
        """
                   Achieve dynamic difficulty. For example, adjusting the difficulty of the 
                   current block dynamically based on the time taken to generate the 
                   previous 10 blocks. 
                   """
        height = len(self.blockchain.blocks)

        if height > 10 and height % 10 == 1:
            dynamic_difficulty = last_block.dynamic_difficulty * \
                                 (self.blockchain.blocks[height - 1].timestamp -
                                  self.blockchain.blocks[height - 10].timestamp) / 5 * 10

        if verified_transactions is None:
            verified_transactions = []

        if proof is None and previous_hash is None:
            previous_hash = last_block.hash
            proof = Chain.proof_of_work(last_block)

        block = Chain.Block(
            height=len(self.blockchain.blocks),
            nonce=proof,
            transactions=verified_transactions,
            previous_block_hash=previous_hash,
            dynamic_difficulty=dynamic_difficulty,
        )
        block.calcHash()  # Calculate current_block_hash
        coinbase_total = block.reward + sum([trans.cached_transaction_fee for trans in verified_transactions])

        # Coinbase Transaction
        coinbase = Transactions.Transaction(
            sender=self.identity,
            outputs=tuple([
                Transactions.TransactionOutput(
                    recipient_address=self.identity,
                    value=coinbase_total,
                    message=None,
                )]
            ),
        )
        coinbase.sign_transaction(self.signer)
        block.transactions.insert(0, coinbase)

        Network.NetworkHandler.get_instance().broadcast_block(block)

        self.blockchain.blocks.append(block)

        # ----------------------------------
        # -- Add all Outputs as new UTXOS --
        # ----------------------------------
        self.blockchain.UTXOs.difference_update(block.extract_STXOs())
        self.blockchain.UTXOs = set(self.blockchain.UTXOs.union(block.extract_UTXOs()))

        # -- UPDATE MY UTXO SET --
        my_utxos = set(block.find_UTXOs(self.identity))
        for my_utxo in my_utxos:
            my_utxo.get_balance(blockchain=self.blockchain)
            # my_utxo.is_valid(sender=None, blockchain=self.blockchain)
        self.my_UTXOs = self.my_UTXOs.union(my_utxos)
        self.store_transactions()
        # ---------------------

        self.blockchain.store_to_file()  # STORE BLOCKCHAIN TO FILE

        # -- UPDATE MY CHAT --
        # -- Yes, it should be implemented a different way... but it is just a demo --
        # -- We are repeating unnecessary calculations
        block.update_chat(self)
        """
        Initialization block.merkle_tree,block.merkle_tree_root
        """
        block.merkle_tree = Chain.MerkleTree(block.transactions)
        block.merkle_tree_root = Chain.MerkleTree(block.transactions).getRootHash()

        return block

    @property
    def is_mining(self):
        return self.__is_mining

    def toggle_mining(self, mine: bool = None):
        self.__is_mining = not self.__is_mining if mine is None else mine

        if self.__is_mining:
            log.info('Started mining...')
            self.__mining_thread.start()
        else:
            log.info('Stopped mining...')
            self.__mining_thread = threading.Thread(target=self.__mine, daemon=True)

    def __mine(self):
        while self.__is_mining:
            self.manual_mine()

    def manual_mine(self) -> Optional[Chain.Block]:
        """
        Mine --WITHOUT TRANSACTION LIMIT--
        :return:
        """
        if not self.verified_transactions:
            return None

        transactions: Dict[str, Transactions.Transaction] = self.verified_transactions
        self.verified_transactions = dict()
        new_block = self.construct_block(
            verified_transactions=list(transactions.values()),
        )
        return new_block

    def add_transaction(self, transaction: Transactions.Transaction) -> bool:
        if not isinstance(transaction, Transactions.Transaction):
            raise ValueError('Transaction is not a valid Transaction object!')

        t_hash = transaction.hash
        if t_hash in self.verified_transactions.keys():
            log.debug(f'[TRANSACTION - {t_hash}] Addition to list rejected (Already verified)')
            return False

        if not transaction.is_valid(blockchain=self.blockchain):  # TODO: , check_utxos=True):
            return False

        self.verified_transactions[t_hash] = transaction
        return True

    def send_message(self, address: str, total_gas: int, total_send: int, message: Messages.AMessage) -> \
            Optional[Transactions.Transaction]:
        t = super().send_message(
            address=address,
            total_gas=total_gas,
            total_send=total_send,
            message=message,
        )

        if t:
            self.add_transaction(t)

        return t
