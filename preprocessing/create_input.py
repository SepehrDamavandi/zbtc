import requests
import json
from bitstring import BitArray



# GENESIS_BLOCK_HASH = '000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f'
# 874944 mod 2016 = 0, /2016 = 434. Difficulty: 108,522,647,629,298.16
GENESIS_BLOCK_HASH = '0000000000000000000140337e0d3e4a14e77b8cbbff0669587903e804ddcef8'

def splitStringFromBack(word, border):
    reverse_word = (word[::-1])
    split_reverse = [reverse_word[i:i+border] for i in range(0, len(reverse_word), border)]
    return list(reversed([i[::-1] for i in split_reverse]))

def littleEndian(string):
    splited = [str(string)[i:i + 2] for i in range(0, len(str(string)), 2)]
    splited.reverse()
    return "".join(splited)

def getBlockHeadersInRange(i,j,url):
    block_hashes = []
    for height in range(i,j):
        block_hashes.append(get_block_hash_by_height(height,url))
    
    block_headers = []
    for bh in block_hashes:
        block_headers.append(get_block_header_by_hash(bh,url))

    return block_headers

def get_block_header_by_hash(block_hash,url):
    payload = {
        "jsonrpc": "2.0",
        "id": "python-client",
        "method": "getblockheader",
        "params": [block_hash]
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["result"]

def getBlocksInRange(i,j,url):
    block_hashes = []
    for height in range(i,j):
        block_hashes.append(get_block_hash_by_height(height,url))
    
    blocks = []
    for bh in block_hashes:
        blocks.append(get_block_by_hash(bh,url))

    return blocks

def get_block_hash_by_height(height,url):
    payload = {
        "jsonrpc": "2.0",
        "id": "python-client",
        "method": "getblockhash",
        "params": [height]
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["result"]
    
def get_block_by_hash(block_hash,url):
    payload = {
        "jsonrpc": "2.0",
        "id": "python-client",
        "method": "getblock",
        "params": [block_hash]
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["result"]

def hexToDecimalZokratesInput(input):
    preimage = bytes.fromhex(input)
    bitarray = BitArray(bytes=preimage)
    return [str(int(i, 2)) for i in splitStringFromBack(bitarray.bin, 128)]


def hexToBinaryZokratesInput(input):
    preimage = bytes.fromhex(input)
    bitarray = BitArray(bytes=preimage)
    return " ".join(bitarray.bin)


def createZokratesInputFromBlock(block):
    version = littleEndian(block['versionHex'])
    little_endian_previousHash = littleEndian(block['previousblockhash']) if block['height'] > 0 else 64 * '0'
    little_endian_merkleRoot = littleEndian(block['merkleroot'])
    little_endian_time = littleEndian(hex(block['time'])[2:])
    little_endian_difficultyBits = littleEndian(block['bits'])
    nonce = hex(block['nonce'])[2:]
    nonce = '0' * (8 - len(nonce)) + nonce #ensure nonce is 4 bytes long
    little_endian_nonce = littleEndian(nonce)

    header = version + little_endian_previousHash + little_endian_merkleRoot + little_endian_time + little_endian_difficultyBits + little_endian_nonce
    return header

# enhance by calling getBlocksInRange once 
def generateZokratesInputFromBlock(first_block, amount, url):
    last_block = first_block + amount
    blocks = getBlockHeadersInRange(first_block, last_block,url)
    epoch_header_block_number = first_block if (first_block+1) % 2016 == 0 else first_block - (first_block % 2016)
    epoch_head = getBlockHeadersInRange(epoch_header_block_number, epoch_header_block_number+1,url) \
        if first_block >= 2016 else getBlockHeadersInRange(0, 1,url)
    epoch_head = hexToDecimalZokratesInput(createZokratesInputFromBlock(epoch_head[0]))
    prev_block_hash = hexToDecimalZokratesInput(littleEndian(getBlockHeadersInRange(first_block-1,first_block, url)[0]["hash"]))
    intermediate_zokrates_blocks = [hexToDecimalZokratesInput(createZokratesInputFromBlock(block)) for block in blocks[0:len(blocks)-1]]
    intermediate_zokrates_blocks = [item for sublist in intermediate_zokrates_blocks for item in sublist] #flatten
    final_zokrates_block = hexToDecimalZokratesInput(createZokratesInputFromBlock(blocks[len(blocks)-1]))
    
    return str([epoch_head[4], *prev_block_hash, *intermediate_zokrates_blocks, *final_zokrates_block]).replace(',','').replace('[','').replace(']','').replace('\'','')


def generateZokratesInputForBlocks(ctx, blocks):
    blocks = [getBlocksInRange(ctx, i, i+1) for i in blocks]
    blocks = [item for sublist in blocks for item in sublist] #flatten
    zokrates_blocks = [createZokratesInputFromBlock(block) for block in blocks[0:len(blocks)]]
    print(str(zokrates_blocks).replace(',','').replace('[','').replace(']',''))


def generateZokratesInputForMerkleProof(ctx, first_block, amount):
    last_block = first_block + amount - 1
    block_hashes = [littleEndian(header) for header in getBlockHeadersInRange(ctx, first_block, last_block+1)]
    joined_blocks = ''.join(block_hashes)
    return hexToBinaryZokratesInput(joined_blocks)
