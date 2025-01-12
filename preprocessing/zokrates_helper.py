#!/usr/bin/env python
import sys
import subprocess
from .create_input import generateZokratesInputFromBlock
from .create_input import generateZokratesInputForMerkleProof

cmd_compute_witness = 'zokrates compute-witness --verbose -a '
cmd_generate_proof = 'zokrates generate-proof'

def validateBatchFromBlockNo(batch_no, batch_size, url):
    print('Getting block information and generating zokrates input...')
    #base_block = 874944
    #result = generateZokratesInputFromBlock(base_block + (batch_no-1)*batch_size+1, batch_size, url)
    result = generateZokratesInputFromBlock((batch_no-1)*batch_size+1, batch_size,url)
    print('Done!')

    print('Exec "{}"'.format(cmd_compute_witness))
    #command = ['/usr/bin/time', '-f', 'Max used memory during exec: %M kbytes']
    command = cmd_compute_witness.split() + result.split()
    subdir = "batch{batch_size}"
    subprocess.run(command, check=True, cwd=subdir)
    print('Done!')

    print('Exec "{}"'.format(cmd_generate_proof))
    command = ['/usr/bin/time', '-f', 'Max used memory during exec: %M kbytes']
    command += cmd_generate_proof.split()
    subprocess.run(command, check=True, cwd=subdir)
    print('Done!')

    command = ['mv', 'witness'] + ['output/witness{}'.format(batch_no)]
    print('Exec "{}"'.format(' '.join(command)))
    subprocess.run(command, check=True, cwd=subdir)
    print('Done!', 'green')

    command = ['mv', 'proof.json'] + ['output/proof{}.json'.format(batch_no)]
    print('Exec "{}"'.format(' '.join(command)), 'cyan')
    subprocess.run(command, check=True, cwd=subdir)
    print('Done!')

def validateBatchesFromBlockNo(batch_no, amountBatches, batch_size, url):
    for i in range(0,amountBatches):
        validateBatchFromBlockNo(batch_no+i*batch_size, batch_size, url)