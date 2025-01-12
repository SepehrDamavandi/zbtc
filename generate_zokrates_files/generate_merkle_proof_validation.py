import math


def generate_create_hash():
    return '''
def create_hash(field[5] preimage) -> bool[256]{
	bool[128] a = unpack128(preimage[0]);
	bool[128] b = unpack128(preimage[1]);
	bool[128] c = unpack128(preimage[2]);
	bool[128] d = unpack128(preimage[3]);
	bool[128] e = unpack128(preimage[4]);

	bool [256] preimage1 = [...a, ...b];
    bool [256] preimage2 = [...c, ...d];
    bool [256] preimage3 = [...[...e, true], ...[false; 127]];
    bool [256] dummy = [...[false; 246], ...[true, false, true, false, false, false, false, false, false, false]]; //second array indicates length of preimage = 640bit

    u32[8] preimage1u32 = bool_to_u32(preimage1);
    u32[8] preimage2u32 = bool_to_u32(preimage2);
    u32[8] preimage3u32 = bool_to_u32(preimage3);
    u32[8] dummyu32 = bool_to_u32(dummy);
    u32[8] intermediary = sha256for1024(preimage1u32, preimage2u32, preimage3u32, dummyu32);
    bool[256] intermediarybool = u32_to_bool(intermediary);
	return u32_to_bool(sha256only(intermediarybool));
}
'''

def generate_merkle_proof_validation_code(number_leafs):
    layers = math.ceil(math.log(number_leafs, 2))
    code = []

    code.append('import "hashes/pedersen/512bitBool.zok" as pedersenhash;')
    code.append('import "utils/pack/bool/pack128.zok" as pack128;')
    code.append('import "utils/pack/bool/unpack128.zok" as unpack128;')
    code.append('import "hashes/sha256/1024bit.zok" as sha256for1024;')
    code.append('import "utils/casts/bool_256_to_u32_8.zok" as bool_to_u32;')
    code.append('import "utils/casts/u32_8_to_bool_256.zok" as u32_to_bool;')
    code.append('import "../sha256only.zok" as sha256only;')

    code.append(generate_create_hash())

    code.append('def main(field[5] preimage, private bool[{layers}][256] path, private field[{layers}] lr) -> field[4]{{'.format(layers=layers))
    code.append('\tbool[256] unpacked_proof_header = create_hash(preimage);')
    code.append('\tbool[256] layer0 = lr[0] == 0 ? pedersenhash([...path[0], ...unpacked_proof_header]) : pedersenhash([...unpacked_proof_header, ...path[0]]);')

    for i in range(1, layers):
        code.append('\tbool[256] layer{i} = lr[{i}] == 0 ? pedersenhash([...path[{i}], ...layer{preceeding}]) : pedersenhash([...layer{preceeding}, ...path[{i}]]);'.format(i=i, preceeding= i-1))

    code.append('\tfield res0 = pack128(layer{layers}[0..128]);'.format(layers=layers-1))
    code.append('\tfield res1 = pack128(layer{layers}[128..256]);'.format(layers=layers-1))

    code.append('\tfield[2] proof_header = [pack128(unpacked_proof_header[0..128]), pack128(unpacked_proof_header[128..256])];')
    code.append('\treturn [...proof_header, res0, res1];')
    code.append('}')

    return '\n'.join(code)