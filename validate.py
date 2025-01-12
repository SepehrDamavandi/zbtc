import subprocess
import preprocessing
import os

def validate(batch_no, multiple_batches, url, batch_size):
    if multiple_batches is not None:
        preprocessing.validateBatchesFromBlockNo(
            batch_no,
            multiple_batches,
            batch_size,
            url
        )
    else:
        print('Getting block information and generating zokrates input...')
        #base_block = 874944
        #result = generateZokratesInputFromBlock(base_block + (batch_no-1)*batch_size+1, batch_size, url)
        result = preprocessing.generateZokratesInputFromBlock((batch_no-1)*batch_size+1, batch_size,url)
        print('Done!')
        print("".join(result))

    v = f'batch{batch_size}/'
    mk = f'batch{batch_size}/mk_tree_validation/'
    o = f'batch{batch_size}/output'
    cmd_witness = ['zokrates', 'compute-witness', '-a']
    cmd_proof = ['zokrates', 'generate-proof']
    cmd_exp = ['zokrates', 'export-verifier']
    cmd_verify = ['zokrates', 'verify']

    try:
       
        print(cmd_witness + result.split())
        result_1 = subprocess.run(cmd_witness + result.split(), cwd=v, text=True, capture_output=True, check=True)
        print(result_1.stdout)

        result_2 = subprocess.run(cmd_proof, cwd=v, text=True, capture_output=True, check=True)
        print(result_2.stdout)

        result_3 = subprocess.run(cmd_exp, cwd=v, text=True, capture_output=True, check=True)
        print(result_3.stdout)

        result_4 = subprocess.run(cmd_verify, cwd=v, text=True, capture_output=True, check=True)
        print(result_4.stdout)

        os.makedirs(o,exist_ok=True)
        command = ['mv', 'witness'] + ['output/witness{batch_no}'.format(batch_no = batch_no)]
        subprocess.run(command, check=True, cwd=v)
        
        command = ['mv', 'proof.json'] + ['output/proof{batch_no}.json'.format(batch_no = batch_no)]
        subprocess.run(command, check=True, cwd=v)

    except subprocess.CalledProcessError as e:
        print(f"Error while executing command: {e.cmd}")
        print("Return Code:", e.returncode)
        print("Error Output:", e.stderr)

        

