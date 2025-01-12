import preprocessing
import subprocess
import os

def create_merkle_proof(block_no, batch_size, url):
    first_block_in_batch = block_no - ((block_no -1) % batch_size)
    block_headers = preprocessing.getBlockHeadersInRange(first_block_in_batch, 
                                                      first_block_in_batch + batch_size, 
                                                      url)
    print(block_headers)
    block_headers = preprocessing.getBlockHeadersInRange(
    first_block_in_batch, 
    first_block_in_batch + batch_size, 
    url
)

# Apply littleEndian to all string values in each header
    block_hashes = [
    {   
        key: preprocessing.littleEndian(value) if isinstance(value, str) else value
        for key, value in header.items()
    }
    for header in block_headers 
    ]

    print(block_hashes)
    target_header_hash = block_hashes[(block_no -1) % batch_size]
    tree = preprocessing.compute_full_merkle_tree(block_hashes)
    header = preprocessing.createZokratesInputFromBlock(preprocessing.getBlockHeadersInRange(block_no, block_no+1,url)[0])
    zokrates_input = preprocessing.get_proof_input(tree, target_header_hash, header)
    

    
    mk = f'batch{batch_size}/mk_tree_validation/'
    o = f'batch{batch_size}/mk_tree_validation/output'

    cmd_witness = ['zokrates', 'compute-witness', '-a']
    cmd_proof = ['zokrates', 'generate-proof']
    cmd_exp = ['zokrates', 'export-verifier']
    cmd_verify = ['zokrates', 'verify']

    os.makedirs(o,exist_ok=True)
    try:
       
        print(zokrates_input.split())
        print(cmd_witness + zokrates_input.split())
        result_1 = subprocess.run(cmd_witness + zokrates_input.split(), cwd=mk, text=True, capture_output=True, check=True)
        print(result_1.stdout)

        result_2 = subprocess.run(cmd_proof, cwd=mk, text=True, capture_output=True, check=True)
        print(result_2.stdout)

        result_3 = subprocess.run(cmd_exp, cwd=mk, text=True, capture_output=True, check=True)
        print(result_3.stdout)

        result_4 = subprocess.run(cmd_verify, cwd=mk, text=True, capture_output=True, check=True)
        print(result_4.stdout)

        os.makedirs(o,exist_ok=True)
        command = ['mv', 'witness'] + ['output/witness{block_no}'.format(block_no = block_no)]
        subprocess.run(command, check=True, cwd=mk)
        
        command = ['mv', 'proof.json'] + ['output/proof{block_no}.json'.format(block_no = block_no)]
        subprocess.run(command, check=True, cwd=mk)

    except subprocess.CalledProcessError as e:
        print(f"Error while executing command: {e.cmd}")
        print("Return Code:", e.returncode)
        print("Error Output:", e.stderr)

    

