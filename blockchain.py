from datetime import datetime
import hashlib
import json


class Blockchain:
    def __init__(self, chain_name, chain_info):
        """
        initiates the chain and creates its genesis block
        :param: chain_name
        :param: chain_info
        """
        self.chain = []
        chain_data = {'Chain Name': chain_name,
                      'Chain Info': chain_info}
        self.genesis_block = self.create_block(data=chain_data, previous_hash='0'*64)

    def create_block(self, data, previous_hash=None):
        """
        creates and mines a block and adds it to the chain
        :param: data: the data to be stored in the block
        :param: previous_hash: the hash of the last block
        :return: the created block
        """
        if previous_hash is None:
            previous_hash = self.chain[-1]['Hash']
        temp_block = self.proof_of_work(data, previous_hash)
        block = {'TimeStamp': str(datetime.now())}
        block.update(temp_block)
        self.chain.append(block)
        return block

    def proof_of_work(self, data, previous_hash):
        """
        solves the cryptographic challenge
        finds the nonce and the hash of the block
        :param: data: the data to be stored in the block
        :param: previous_hash: the hash of the last block
        :return: parts of the final block
        """
        nonce = 0
        check_proof = False
        block = {'Index': len(self.chain) + 1,
                 'Nonce': None,
                 'Data': data,
                 'Previous Hash': previous_hash}
        while check_proof is False:
            block['Nonce'] = nonce
            current_hash = Blockchain.calculate_hash(block)
            if current_hash[:4] == '0000':
                check_proof = True
                block['Hash'] = current_hash
            else:
                nonce += 1
        return block

    @staticmethod
    def calculate_hash(block):
        """
        calculates the hash of a given block
        :param: block: the given block
        :return: the hash of the given block
        """
        encoded_block = json.dumps(block).encode()
        current_hash = hashlib.sha256(encoded_block).hexdigest()
        return current_hash

    @staticmethod
    def is_valid(chain):
        """
        checks the validity of a given chain
        by checking the hashes and their link
        :param: chain: the given chain
        :return: a flag that indicates the validity
        """
        previous_hash = '0'*64
        for block in chain:
            temp = {}
            temp.update(block)
            del temp['TimeStamp']
            if temp['Previous Hash'] != previous_hash:
                return False
            current_hash = temp.pop('Hash')
            if Blockchain.calculate_hash(temp) != current_hash:
                return False
            previous_hash = current_hash
        return True
