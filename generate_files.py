import os
import shutil
import sys
import preprocessing
import generate_zokrates_files as zokrates_file_generator

def generate_files(batch_size):
    p = 'batch{batch_size}'.format(batch_size=batch_size)
    pp = 'batch{batch_size}/mk_tree_validation'.format(batch_size=batch_size)
    os.makedirs(p,exist_ok=True)
    os.makedirs(pp,exist_ok=True)
    shutil.copy('sha256only.zok',p)
    shutil.copy('sha256only.zok',pp)
    shutil.copy('getHexLength.zok',p)

    zokrates_file_generator.write_zokrates_file(zokrates_file_generator.generate_validation_code(batch_size), "batch{i}/validate.zok".format(i=batch_size))
    zokrates_file_generator.write_zokrates_file(zokrates_file_generator.generate_root_code(batch_size), "batch{i}/compute_merkle_root.zok".format(i=batch_size))
    zokrates_file_generator.write_zokrates_file(zokrates_file_generator.generate_merkle_proof_validation_code(batch_size), "batch{i}/mk_tree_validation/verify_merkle_proof.zok".format(i=batch_size))