import requests
import json
from validate import validate
from generate_files import generate_files 
from setup import setup
from create_merkle_proof import create_merkle_proof

# API endpoint with embedded token
url = "https://go.getblock.io/b91403bca19e48aa9b014eb6d50a2f76"


generate_files(4)
setup(4)
validate(2,multiple_batches=None,url=url,batch_size=4)
validate(batch_no=1,url=url,batch_size=4,multiple_batches=None)
#create_merkle_proof(7,4,url)
