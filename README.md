run 

``` bash
$  python3 -m venv venv
$ . venv/bin/activate
```
to setup a virtual environment

the run 
``` bash
$  pip3 install -r requirements.txt
```
to install zokrates please run

```bash
$  curl -LSfs get.zokrat.es | sh
```
if you already have installed zokrates but command is unknown run

```bash
$  export PATH=$PATH:/home/{username}/.zokrates/bin
```
for now just edit the zbtc.py file to run different stages and functionalities of the program
default batch_size is 4

stages:

1. generating .zok files for our circuits namely validate.zok which confirms block batches of size n
    and verify_merkle_proof.zok which proofs correct membership for an intermediary block of batch size n validation setting.

    uncomment the generate_files line in the program and edit the defaults.

2. setuping for our circuits 

3. validate.py can generate proofs for any batch number, provide an API endpoint token for this function

4. create_merkle_proof is to be used for transaction confirmation and intermediary block confirmation. Its yet incomplete

Notice: Compilation for larger batch_size could lead to stack overflow of RAM or crash of the program. Try for your max, batch size of 32 can run on a typical mining server and requires batch proof generation every ~6 hour.

## License

This software is licensed under the GNU Lesser General Public License v3 (LGPL-3.0). 
The minimal corresponding source is available at [https://github.com/informartin/zkRelay].