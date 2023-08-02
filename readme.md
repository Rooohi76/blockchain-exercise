# Simple Blockchain Exercise Project

Welcome to the Simple Blockchain Exercise Project! This project aims to provide a basic implementation of a blockchain using a simple proof-of-work consensus algorithm. It serves as a starting point for understanding the fundamental concepts behind blockchain technology.

## Getting Started

To get started with the project, follow these steps:

1. Clone the repository: `git clone https://github.com/Rooohi76/blockchain-exercise.git`
2. Navigate to the project directory: `cd blockchain-exercise`
3. Install the necessary dependencies: `pip install -r requirements.txt`
4. Start the blockchain node: `python main.py`

The blockchain node will be up and running, and you can interact with it by making HTTP requests using Postman API.

## How to use

This simple blockchain exercise project is designed to store email threads in multiple chains, one email per block and can be used like this:

- To create and initialize a new chain: `url/create_chain?chain_name=name&chain_info=info`
- To mine a new block in a chain: `url/mine_block?chain_name=name&sender=sender&receiver=receiver&subject=subject&message=message`
- To view the chain containing a specific email thread: `url/get_chain?chain_name=name`
- To view all chains and their specifications: `url/get_chains`
- To check the validation of a chain: `url/check_validity?chain_name=name`
