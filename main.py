from flask import Flask, jsonify, request
from blockchain import Blockchain

# To store as many blockchains as we want and work on them simultaneously
blockchains = {}

# Initiate a Flask object with the name of module to start
app = Flask(__name__)
app.json.sort_keys = False


def wrap_data(sender, receiver, subject, message):
    """
    wraps the information of the message we want to put in a block
    :param: sender
    :param: receiver
    :param: subject
    :param: message
    :return: a dict containing information of the message
    """
    data = {'From': sender,
            'To': receiver,
            'Subject': subject,
            'Message': message}
    return data


@app.route('/create_chain', methods=['GET'])
def create_chain():
    """
    gets a chain name and a chain info from user to initialize a chain
    and put it into the list of chains.
    should be used like this:
    url/create_chain?chain_name=name&chain_info=info
    :return: a jsonified response with a status message and genesis block
    to show to user. also an HTTP status code
    """
    chain_name = request.args.get('chain_name')
    chain_info = request.args.get('chain_info')
    blockchain = Blockchain(chain_name, chain_info)
    blockchains[chain_name] = blockchain
    response = {'Status': 'You created a chain successfully!'}
    response.update(blockchain.genesis_block)
    return jsonify(response), 200


@app.route('/mine_block', methods=['GET'])
def mine_block():
    """
    gets a chain name and content of the message to store from user
    wraps the content of the message using wrap_data()
    mines a block to store the data and adds it into the specified chain
    should be used like this:
    url/mine_block?chain_name=name&sender=sender&receiver=receiver \
    &subject=subject&message=message
    :return: a jsonified response with a status message and mined block
    to show to user. also an HTTP status code
    """
    chain_name = request.args.get('chain_name')
    sender = request.args.get('sender')
    receiver = request.args.get('receiver')
    subject = request.args.get('subject')
    message = request.args.get('message')
    blockchain = blockchains[chain_name]
    data = wrap_data(sender, receiver, subject, message)
    block = blockchain.create_block(data)
    response = {'Status': 'You mined a block successfully!'}
    response.update(block)
    return jsonify(response), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
    """
    gets a chain name from user and shows the specified chain
    should be used like this:
    url/get_chain?chain_name=name
    :return: a jsonified response with the length of the specified chain
    and its blocks to show to user and an HTTP status code
    """
    chain_name = request.args.get('chain_name')
    blockchain = blockchains[chain_name]
    response = {'Length': len(blockchain.chain),
                'Chain': blockchain.chain}
    return jsonify(response), 200


@app.route('/get_chains', methods=['GET'])
def get_chains():
    """
    shows the number of blockchains we have
    and also shows the length of each chain and its genesis blocks
    should be used like this:
    url/get_chains
    :return: a jsonified response with the number of the chains
    and their length and genesis block to show to user
    and an HTTP status code
    """
    chains = []
    keys = blockchains.keys()
    for key in keys:
        temp = {'Length': len(blockchains[key].chain),
                'Chain': blockchains[key].genesis_block}
        chains.append(temp)
    response = {'Count': len(blockchains),
                'Chains': chains}
    return jsonify(response), 200


@app.route('/check_validity', methods=['GET'])
def check_validity():
    """
    gets a chain name from user and checks its validity
    should be used like this:
    url/check_validity?chain_name=name
    :return: a jsonified response with the relevant status message
    and an HTTP status code
    """
    chain_name = request.args.get('chain_name')
    blockchain = blockchains[chain_name]
    check = Blockchain.is_valid(blockchain.chain)
    if check is True:
        status = f'The blockchain {chain_name} is valid!'
    else:
        status = f'The blockchain {chain_name} is invalid!'
    response = {'Status': status}
    return jsonify(response), 200


# Runs the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
