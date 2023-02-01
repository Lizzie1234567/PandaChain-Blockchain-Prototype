import time
import bc as Unc
import bc.nodes as Nodes
import bc.network as Network
import logging


logging.getLogger().setLevel(logging.DEBUG)


def tst_run(port=5000):
	# Unc.my_node = Nodes.Client(Nodes.KeyFactory.load_or_generate_key())
	#
	# from Crypto.Cipher import AES, PKCS1_OAEP
	# import binascii
	#
	# public_key = Unc.my_node.identity
	# from Crypto.PublicKey import RSA
	# from Crypto.Random import get_random_bytes
	#
	# session_key = get_random_bytes(16)
	#
	# cipher_rsa = PKCS1_OAEP.new(
	# 	RSA.import_key(binascii.unhexlify(public_key))
	# )
	# enc_session_key = cipher_rsa.encrypt(session_key)
	# # enc_session_key = binascii.hexlify(enc_session_key).decode('ascii')
	#
	# cipher_aes = AES.new(session_key, AES.MODE_EAX)
	# ciphertext, tag = cipher_aes.encrypt_and_digest('hello_msg'.encode('utf-8'))
	# encoded_text = b''.join([x for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)])
	# print(encoded_text)
	# IO.
	# enc_session_key, nonce, tag, ciphertext = \
	# 	[encoded_text. for x in (Unc.my_node.private_key.size_in_bytes(), 16, 16, -1)]
	#
	# cipher_rsa = PKCS1_OAEP.new(Unc.my_node.private_key)
	# session_key = cipher_rsa.decrypt(enc_session_key)
	#
	# cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
	# data = cipher_aes.decrypt_and_verify(ciphertext, tag)
	#
	# print(data.decode('utf-8'))




	Network.PeerNetwork.load_from_file()
	Network.NetworkHandler.get_instance(
		my_peer=Network.Peer(
			address='127.0.0.1',
			port=port
		)
	)
	time.sleep(1)

	import bc.web.views
	import bc.web.api
	bc.app.run(port=port)


# def run(port=5000):
# 	# key = menus.menu_select_key()
# 	# my_node = menus.menu_select_client_type(key, my_peer=Nodes.Peer("127.0.0.1", port))
# 	Unc.my_node = Nodes.Miner(Nodes.KeyFactory.create_key())
#
# 	# -- START WEB SERVER --
# 	print('Good to go... Starting web server...')
# 	import bc.web
# 	w = threading.Thread(target=Unc.app.run, args=(None, port,), daemon=True)
# 	w.start()
# 	# ----------------------
#
# 	time.sleep(1)
# 	while True:
# 		time.sleep(5)
# # 	# -- START MENU --
# # 	time.sleep(1)
# # 	while True:
# # 		menus.menu_main(my_node)
# #


if __name__ == '__main__':
	port = int(input('Please provide port number: '))
	# port = 5000
	tst_run(port)
	# key = Nodes.KeyFactory.load_key('WICKED')
	# miner = Nodes.Miner(private_key=key)
	# print('Miner priv\t\t: ', miner.private_key)
	# print('Miner pub\t: ', miner.public_key)
	# print('Miner ide\t: ', miner.identity)
	#
	# miner._construct_genesis_block()
	# print(miner.blockchain)
	# print(miner.blockchain.is_valid(
	# 	lite=False
	# ))
	#
	# T_OUT = Transactions.TransactionOutput(
	# 	recipient_address=miner.identity,
	# 	value=42,
	# 	message=Messages.TextMessage('Hello there...General Kenobi')
	# )
	# print(T_OUT)
	#
	# T_IN = Transactions.TransactionInput(
	# 	block_index=0,
	# 	transaction_index=0,
	# 	output_index=0,
	# )
	#
	# print('T_IN_valid:', T_IN.is_valid(
	# 	sender=miner.identity,
	# 	blockchain=miner.blockchain
	# ))
	#
	# T = Transactions.Transaction(
	# 	sender=miner.identity,
	# 	inputs=(T_IN, ),
	# 	outputs=(T_OUT, ),
	# )
	#
	# T.sign_transaction(miner.signer)
	#
	# print(
	# 	T.is_valid(
	# 		blockchain=miner.blockchain
	# 	)
	# )
	#
	# miner.add_transaction(T)
	# miner.manual_mine()
	# print(miner.blockchain)
	# print(miner.blockchain.is_valid(
	# 	lite=False
	# ))

