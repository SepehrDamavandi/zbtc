import math

def generate_compute_root(number_leafs):
    if number_leafs > 2:
        output = '\tbool[{len}][256] layer{layer} = [\n'.format(len=math.ceil(number_leafs/2), layer=(math.ceil(math.log(number_leafs,2))-1))
    else:
        output = '\tbool[256] layer{layer} = '.format(layer=(math.ceil(math.log(number_leafs,2))-1))
    for i in range(0, number_leafs-2, 2):
        output = output + '\t\tpedersenhash([...layer{layer}[{a}], ...layer{layer}[{b}]]),\n'.format(a=i, b=i+1, layer=math.ceil(math.log(number_leafs,2)))
    output = output + '\t\tpedersenhash([...layer{layer}[{a}], ...layer{layer}[{b}]])'.format(a=number_leafs-2 if number_leafs % 2 == 0 else number_leafs-1, b=number_leafs-1, layer=math.ceil(math.log(number_leafs,2)))
    if number_leafs < 3:
        output = output + ';\n'
    if number_leafs > 2:
        output = output + '\t];\n'

    if number_leafs > 2:
        output = output + generate_compute_root(math.ceil(number_leafs/2))

    return output

def generate_root_code(number_leafs):
    output = ('import "hashes/pedersen/512bitBool.zok" as pedersenhash;\nimport "utils/pack/bool/pack128.zok" as pack128;\nimport "utils/pack/bool/unpack128.zok" as unpack128;\n' +
        '\ndef main(bool[{number_leafs}][256] layer2) -> field[{layer}]{{\n'.format(number_leafs=number_leafs,layer=math.ceil(math.log(number_leafs,2))) +
        generate_compute_root(number_leafs) +
        '\tfield res0 = pack128(layer0[0..128]);\n' +
        '\tfield res1 = pack128(layer0[128..256]);\n' +
        '\treturn [res0, res1];\n'+
        '\t}')
    return output