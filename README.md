# PandaChain-Blockchain-Prototype
 UTXO-based peer-to-peer network interaction Blockchain Prototype
 
Based on Bitcoin, created a blockchain prototype with UTXO-based peer-to-peer network interaction, PoW 
consensus method, dynamic difficulty adjustment, RSA encryption, and MongoDB storage. And achieved 51% 
attack and double-spend attack

3.2 Core content in our design
In our design, two main parts in a transaction are also implemented. They are P2PKH and UTXO.
3.2.1 P2PKH

Pay-to-PubKey-Hash (Pay-to-Public-Key-Hash, P2PKH) is the normal form of a transaction. In the P2PKH, we have the transaction input, transaction output and signature. Transactions that pay to an address contain P2PKH scripts that are resolved by sending the public key and a digital signature created by the corresponding private key. 
There are two reasons why Nakamoto later decided to use P2PKH rather than P2PK. 

First, elliptic curve encryption (encryption used by public and private keys) will be influenced by the modified Shor algorithm, which means that quantum computers may be able to retrieve private keys from public keys in the future. 

And second, the hash value is smaller, so it is easier to print and embed in small storage media such as QR codes.

Here are some parts of our code, which contain the input, output and signature.
 


 
Signature

In this way, the node can verify the signature with the public key. The payment that A makes in a transaction, is the payment to someone's public key, which is the payment to P2PKH address.

3.2.2 UTXO
The UTXO is the unspent transaction output, which is invented by Satoshi Nakamoto who is also the inventor of Bitcoin. We all know that the records in Bitcoin are not the money or the coin, but the transactions consisting of inputs and outputs. Every transaction has its input and gets its output. The database will store all the UTXO so that if we spend our Bitcoin, it actually is we spend our UTXO and get a new UTXO, which will be locked by the receiver’s public key hash. 
Here is our design. In this part, first, retrieve the UTXO from the cache, and choose the one whose balance is >=(greater than or equal to )the total gas+ total send by using the code following: “if allocated_balance >= total_gas + total_send; break”.
Then the transaction output will be regarded as the transaction input of the new one. And delete the transaction output from the current UTXO, and finally add it to the STXO.
 
     
UTXO
4. Network
4.1 Core content in our design
The core contents are the movement of broadcasting to the peer-to-peer network, method of getting a new block and block validation.
4.1.1 Broadcast
In a large decentralized network like Bitcoin, each time a new block is generated, information will be transmitted according to the Gossip protocol. If a node occupies a new valid block, it notifies the other nodes connecting to it. And then the block will be transferred to those nodes that it is asked to do. Before a block reaches each full node in the network, it passes through multiple intermediate nodes. And each node verifies the block before forwarding it to other peer nodes. 
Here is our design. We design to get a JSON file and set a request to the web page by ”jason_data= request.get_json”. If the data is none, it shows the message of ‘incorrect Json data’ and an error code of 400. Then it loads the json_data as data, and assigns the data to block by the following: ”Chain.Block.from_json(data)”. If the hash of the block exists, it shows the message ‘Already processed’. Otherwise, it appends the hash of the block to the my_node file and records it with the block height. By implementing “my_node.blockchain.size != 0 and block.is_valid()”, there is a situation that the block size is not 0, and the function ‘is_valid’ will be called to judge whether it is valid or not, which uses 3 parameters.
 
Broadcast

4.1.2 Get block
The basic design idea of getting a block is that: 
First, the node client constructs the block, and then sends the block header data to the external mining program. The mining program traverses the nonce for mining, delivers it back to the node client after verification, and broadcasts it to the whole network after verification.
In our design, if the context of q is not empty, it will proceed with ”block: Chain.Block= q.get(timeout=1)” and will record the block height along with the ‘Broadcasting Block’. Next, the JSON data in the block will be read and decoded in the form of ‘utf-8’ and then given to ‘data’. If the data is empty, the block height will be recorded and ‘Broadcasting Block failed. Bad JSON ’ will be shown as well. Then, assign the broadcast JSON data to ‘total_sent’ and ‘total_peers’ with three parameters. Finally, log the block height and both the ‘total_sent’ and ‘total_peers’. 
 
Get block

4.1.3 Validation
Validation should be made to ensure that the blocks we received from other miners are valid. There are several validations in the traditional validation process. First, the data structure of the block is syntactically valid. Second, they verify proof of work that the hash value of the block header is less than the target difficulty (verify that sufficient proof of work is included). What’s more, the block timestamp is two hours ahead of the validation time (time error allowed). Besides, whether the block size is within the length limit is also verified. Last but not least, the first trade (and only the first) is a coinbase trade.
In our design, we also verify the following items: whether the height of the current block is bigger than the previous one, whether the time is later, whether the dynamic difficulty is satisfied, as well as the coinbase is valid or not. 
Especially, whether the hash in a block is equal to the previous one is the most significant part. The code following to recalculate the hash will be implemented: “elif not lite and self. previous_block_hash != prev_block.hash”, and the result of ‘verification Failure’ on our page will appear.
 
 
Validation

5. Storage
MongoDB is a NoSQL database developed by 10gen, which stands for Not Only SQL, and was first released in 2009 (What is MongoDB?, n.d.). Specifically, MongoDB is a document-oriented database developed in C++ where the relevant objects are recorded in a single document and each document is schema-free, thus MongoDB is more flexible. Data is stored in binary format in BSON. However, this brings certain data redundancy and storage overhead.

On the one hand, MongoDB also has the characteristics of a relational database. Its query language library is very rich and has object-oriented syntax features. At the same time, it also provides related interfaces such as indexing, so users can easily interact with MongoDB. Therefore, MongoDB can use the experience of traditional relational databases to use MongoDB's index. On the other hand, MongoDB has the advantages of non-relational databases, provides a very loose data structure, and can support more complex and rich data types than relational databases. The storage approach in MongoDB is document-based. In When using MongoDB to store data files, users do not need to define their document structure in advance, because it allows files with different structures to be stored in the same database.

Using MongoDB in the blockchain system can enrich the data query processing function of the blockchain system and expand the application scenarios of the blockchain system (Bandara et al., 2018). In scenarios where the table structure is unclear and the data is constantly changing, the unstructured nature of MongoDB makes it easy to expand fields without affecting the original data (Bandara et al., 2021). In scenarios with extremely high write loads, MongoDB's high write performance makes it more suitable for business systems with a large amount of "low-value" data written. In the scenario where the amount of data continues to grow, if MySQL is used in the blockchain system, in order to avoid performance degradation. The forms in the database need to be split horizontally or vertically, which is very inconvenient, and the sharding feature of MongoDB can make it better adapt to the situation of massive data growth.
	FileSystem+levelDB	MySQL	MongoDB
Extensibility	Poor	The table structure is clear and easy to expand	Good
Specified field query	Key， blockNum， blockHash and other limited fields	All the fields	All the fields
Query feature richness	Single	Abundant	More abundant
So, our project uses the MongoDB to store the raw data of the whole blockchain. 
 
For, the latest state (e.g., sender, input, timestamp), our project uses dict which comes from Dict package to store various blockchain related information into memory. 
 
6. Attack
In the fast payment scenario, since it takes a certain amount of time for the transaction to be confirmed by the Bitcoin system, the victim usually sends an item of a certain value to the attacker before the transaction is confirmed. This makes it easy for an attacker to implement a double-spending attack (Karame et al., 2012).

The 51% attack can recover the spent digital currency or use it multiple times, mainly targeting blockchains based on the PoW consensus mechanism (Shanaev et al., 2019). A 51% attack is generally divided into 4 steps:

① The attacker initiates a transaction A to transfer a certain amount of digital cryptocurrency to the victim;

② After receiving enough confirmations from transaction A, the victim approves transaction A and hands over property of equivalent value to the attacker;

③After obtaining the property, the attacker creates a fork from the block before transaction A, and uses more than 51% of the computing power advantage to mine on the fork chain;

④ When the length of the forked chain exceeds the original main chain, it becomes the new main chain according to the longest chain principle, the transaction A on the original main chain is invalid, and the attack is successful (Yang et al., 2019).

Double-spend attack, that is, an attack in which the same digital currency is spent multiple times (Pérez-Solà et al., 2019). A double-spending attack consists of the following 4 steps:

① The attacker’s address AA initiates a transaction A to transfer digital currency to the victim;

②The victim approves transaction A after receiving enough confirmations in transaction A, and transfers cash or sends goods to the attacker;

③The attacker’s address AA initiates a transaction B to transfer digital currency to its address AB, and the transaction amount is the total amount of digital currency in the attacker’s address AA. Because transaction A conflicts with transaction B, the blockchain forks;

④The attacker uses various methods (51% attack, bribery attack, and eclipse attack) to make the chain containing transaction B longer than the chain containing transaction A. According to the longest chain principle, transaction B is considered valid, while transaction A is considered invalid and the attacker succeeds (Rosenfeld, 2014).

This is a schematic diagram of our project implementing 51% attack and double-spending attack. 
 
 ![image](https://user-images.githubusercontent.com/48409053/215999476-654b2db0-dddd-4905-8403-99273d07ffdf.png)

Figure 1: 51% attack and double-spending attack.

Under the condition that the computing power is guaranteed to be the same, two honest miners out of five miners maintain a main chain.  
 
 ![image](https://user-images.githubusercontent.com/48409053/215999531-fd88c193-5ed5-4e4e-938a-bcffb2b00414.png)

Figure 2: Before attack.

And the other three miners attack and create a longer corrupt chain.
 
 ![image](https://user-images.githubusercontent.com/48409053/215999595-17c34145-af11-4ac5-ad49-8dd07e0439cb.png)

Figure 3: Attacks were carried out.

When the corrupt chain exceeds the main chain, according to the longest chain principle, the main chain maintained by honest miners is abandoned. At this point, the 51% attack is complete. 

![image](https://user-images.githubusercontent.com/48409053/215999649-4809ab6f-731a-4440-b5d7-e53b1077cd03.png)

Figure 4: After attack.
