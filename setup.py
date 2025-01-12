
import subprocess
def setup(batch_size):

    p = f'batch{batch_size}/'
    pp = f'batch{batch_size}/mk_tree_validation/'  
    command1 = ['zokrates', 'compile', '-i', 'validate.zok']
    command2 = ['zokrates', 'compile', '-i', 'verify_merkle_proof.zok']
    command3 = ['zokrates', 'setup']

    try:
       
        result_1 = subprocess.run(command1, cwd=p, text=True, capture_output=True, check=True)
        print(result_1.stdout)

        result_2 = subprocess.run(command2, cwd=pp, text=True, capture_output=True, check=True)
        print(result_2.stdout)

        result_3 = subprocess.run(command3, cwd=p, text=True, capture_output=True, check=True)
        print(result_3.stdout)

        result_4 = subprocess.run(command3, cwd=pp, text=True, capture_output=True, check=True)
        print(result_4.stdout)

    except subprocess.CalledProcessError as e:
        print(f"Error while executing command: {e.cmd}")
        print("Return Code:", e.returncode)
        print("Error Output:", e.stderr)
    

