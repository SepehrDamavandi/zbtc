def generate_validation_code(n_blocks):
    static_code = """import "utils/pack/bool/pack128.zok" as pack128;
import "utils/pack/u32/pack128.zok" as pack128u32;
import "utils/pack/bool/unpack128.zok" as unpack128;
import "utils/pack/u32/unpack128.zok" as unpack128u32;
import "utils/pack/bool/pack256.zok" as pack256bool;
import "utils/pack/u32/pack256.zok" as pack256u32;
import "utils/pack/bool/unpack256.zok" as unpack256bool;
import "utils/pack/u32/nonStrictUnpack256.zok" as unpack256u32;
import "hashes/sha256/1024bit.zok" as sha256for1024;

import "utils/casts/field_to_u32.zok" as field_to_u32;
import "utils/casts/u32_to_field.zok" as u32_to_field;
import "utils/casts/bool_256_to_u32_8.zok" as bool_to_u32;
import "utils/casts/u32_8_to_bool_256.zok" as u32_to_bool;
import "utils/casts/bool_128_to_u32_4.zok" as bool_to_u32_128;
import "utils/casts/u32_4_to_bool_128.zok" as u32_to_bool_128;

import "./sha256only.zok" as sha256only;
import "./getHexLength.zok" as getHexLength;
import "./compute_merkle_root.zok" as compute_merkle_root;

def toBigEndian32bit(bool[32] value) -> bool[32]{
    return [
            ...value[24..32],
            ...value[16..24],
            ...value[8..16],
            ...value[0..8]];
}

def toBigEndian24bit(bool[24] value) -> bool[24]{
    return [
            ...value[16..24],
            ...value[8..16],
            ...value[0..8]];
}

def toBigEndian128bit(bool[128] value) -> bool[128]{
    return [
            ...value[120..128],
            ...value[112..120],
            ...value[104..112],
            ...value[96..104],
            ...value[88..96],
            ...value[80..88],
            ...value[72..80],
            ...value[64..72],
            ...value[56..64],
            ...value[48..56],
            ...value[40..48],
            ...value[32..40],
            ...value[24..32],
            ...value[16..24],
            ...value[8..16],
            ...value[0..8]];
}

def packMaxVariance(field length) -> field{
    field mut result = 0;
    result = length == 1 ? pack128([...[false; 124], ...[true; 4]]) : result;
    result = length == 2 ? pack128([...[false; 120], ...[true; 8]]) : result; 
    result = length == 3 ? pack128([...[false; 116], ...[true; 12]]) : result;
    result = length == 4 ? pack128([...[false; 112], ...[true; 16]]) : result;
    result = length == 5 ? pack128([...[false; 108], ...[true; 20]]) : result;
    result = length == 6 ? pack128([...[false; 104], ...[true; 24]]) : result;
    result = length == 7 ? pack128([...[false; 100], ...[true; 28]]) : result;
    result = length == 8 ? pack128([...[false; 96], ...[true; 32]]) : result;
    result = length == 9 ? pack128([...[false; 92], ...[true; 36]]) : result;
    result = length == 10 ? pack128([...[false; 88], ...[true; 40]]) : result;
    result = length == 11 ? pack128([...[false; 84], ...[true; 44]]) : result;
    result = length == 12 ? pack128([...[false; 80], ...[true; 48]]) : result;
    result = length == 13 ? pack128([...[false; 76], ...[true; 52]]) : result;
    result = length == 14 ? pack128([...[false; 72], ...[true; 56]]) : result;
    result = length == 15 ? pack128([...[false; 68], ...[true; 60]]) : result;
    result = length == 16 ? pack128([...[false; 64], ...[true; 64]]) : result;
    result = length == 17 ? pack128([...[false; 60], ...[true; 68]]) : result;
    result = length == 18 ? pack128([...[false; 56], ...[true; 72]]) : result;
    result = length == 19 ? pack128([...[false; 52], ...[true; 76]]) : result;
    result = length == 20 ? pack128([...[false; 48], ...[true; 80]]) : result;
    result = length == 21 ? pack128([...[false; 44], ...[true; 84]]) : result;
    result = length == 22 ? pack128([...[false; 40], ...[true; 88]]) : result;
    result = length == 23 ? pack128([...[false; 36], ...[true; 92]]) : result;
    result = length == 24 ? pack128([...[false; 32], ...[true; 96]]) : result;
    result = length == 25 ? pack128([...[false; 28], ...[true; 100]]) : result;
    result = length == 26 ? pack128([...[false; 24], ...[true; 104]]) : result;
    result = length == 27 ? pack128([...[false; 20], ...[true; 108]]) : result;
    result = length == 28 ? pack128([...[false; 16], ...[true; 112]]) : result;
    result = length == 29 ? pack128([...[false; 12], ...[true; 116]]) : result;
    result = length == 30 ? pack128([...[false; 8], ...[true; 120]]) : result;
    result = length == 31 ? pack128([...[false; 4], ...[true; 124]]) : result;
    result = length == 32 ? pack128([true; 128]) : result;
return result;
}


def packTarget(bool[32] bits) -> field {
    field compare = pack128([...[false;120], ...bits[0..8]]);
    field result = 
    if (compare == 23) {pack128([...[false; 72], ...bits[8..32], ...[false; 32]])} else {
      if (compare == 24) {pack128([...[false; 64], ...bits[8..32], ...[false; 40]])} else {
        if (compare == 25) {pack128([...[false; 56], ...bits[8..32], ...[false; 48]])} else {
          if (compare == 26) {pack128([...[false; 48], ...bits[8..32], ...[false; 56]])} else {
            if (compare == 27) {pack128([...[false; 40], ...bits[8..32], ...[false; 64]])} else {
              if (compare == 28) {pack128([...[false; 32], ...bits[8..32], ...[false; 72]])} else {
                if (compare == 29) {pack128([...[false; 24], ...bits[8..32], ...[false; 80]])} else {
                  if (compare == 30) {pack128([...[false; 16], ...bits[8..32], ...[false; 88]])} else {
                    if (compare == 31) {pack128([...[false; 8], ...bits[8..32], ...[false; 96]])} else {
                        pack128([false; 128])
                    }
                  }
                }
              }
            }
          }
        }
      }
    };            
    return result;
}

def get_bit_length_bits(bool[24] bits) -> field{
    field mut result = 0;
    for u32 i in 0..24 {
        result = (result == 0) && (bits[i] == true) ? u32_to_field(24-i) : result;
    }
return result;
}

def get_hex_length_bits(bool[24] bits) -> field{

    field bit_length = get_bit_length_bits(bits);
    field mut result = 0;
    result = bit_length > 0 ? 1 : result;
    result = bit_length > 4 ? 2 : result;
    result = bit_length > 8 ? 3 : result;
    result = bit_length > 12 ? 4 : result;
    result = bit_length > 16 ? 5 : result;
    result = bit_length > 20 ? 6 : result;

return result;
}

// call with last field of block array
def validate_target(field epoch_head, field epoch_tail, field next_epoch_head) -> (bool,field){
    bool[128] epoch_head_unpacked = unpack128(epoch_head);
    bool[128] epoch_tail_unpacked = unpack128(epoch_tail);
    bool[128] next_epoch_head_unpacked = unpack128(next_epoch_head);
    field time_head = pack128([...[false; 96], ...toBigEndian32bit(epoch_head_unpacked[32..64])]);
    field time_tail = pack128([...[false; 96], ...toBigEndian32bit(epoch_tail_unpacked[32..64])]);   

    field current_target = packTarget(toBigEndian32bit(epoch_head_unpacked[64..96]));
    field time_delta = time_tail - time_head;
    field target_time_delta = 1209600; // 2016 * 600 (time interval of 10 minutes)

    field mut target = current_target * time_delta; // target_time_delta

    field encoded_target = packTarget(toBigEndian32bit(next_epoch_head_unpacked[64..96]));
    field encoded_target_extended = encoded_target * target_time_delta;

    // The encoding of targets uses a floor function, the comparison of a calculated target may therefore fail
    // Therefore, a maximum variance is calculated that is one hex digit in the encoding
    field maxVariance = packMaxVariance(getHexLength(target)-get_hex_length_bits(toBigEndian24bit(next_epoch_head_unpacked[64..88])));
    // int('ffff' + 10 * '00', 16) * 2016 * 600 = 95832923060582736897701037735936000
    target = target > 95832923060582736897701037735936000 ? 95832923060582736897701037735936000 : target;
    field mut delta = target - encoded_target_extended;
    delta = target >= encoded_target_extended ? delta : maxVariance + 1;
    bool valid = delta <= maxVariance ? true : false;
    //field valid = if (37202390668975264121251936602161152-81015268229227203625641762304819200) < 1267650600228229401496703205375 then 1 else 0 fi
return (valid, current_target);
}

def hash_block_header(field[5] preimage) -> u32[8]{
    bool[128] a = unpack128(preimage[0]);
    bool[128] b = unpack128(preimage[1]);
    bool[128] c = unpack128(preimage[2]);
    bool[128] d = unpack128(preimage[3]);
    bool[128] e = unpack128(preimage[4]);

    bool[256] preimage1 = [...a, ...b];
    bool[256] preimage2 = [...c, ...d];
    bool[256] preimage3 = [...[...e, true], ...[false; 127]];
    bool[256] dummy = [...[false; 246], ...[true, false, true, false, false, false, false, false, false, false]]; //second array indicates length of preimage = 640bit

    u32[8] intermediary = sha256for1024(bool_to_u32(preimage1), bool_to_u32(preimage2), bool_to_u32(preimage3), bool_to_u32(dummy));

    u32[8] r = sha256only(u32_to_bool(intermediary));
    return r;
}

def validate_block_header(field reference_target, bool[256] bin_prev_block_hash, field[5] preimage) -> bool[257]{
    bool[128] a = unpack128(preimage[0]);
    bool[128] b = unpack128(preimage[1]);
    bool[128] c = unpack128(preimage[2]);
    bool[128] d = unpack128(preimage[3]);
    bool[128] e = unpack128(preimage[4]);

    field encoded_prev_block_hash1 = pack128([...a[32..128], ...b[0..32]]);
    field encoded_prev_block_hash2 = pack128([...b[32..128], ...c[0..32]]);
    field[2] prev_block_hash = [pack128(bin_prev_block_hash[0..128]), pack128(bin_prev_block_hash[128..256])];
    bool mut valid = encoded_prev_block_hash1 == prev_block_hash[0] && encoded_prev_block_hash2 == prev_block_hash[1] ? true : false;

    // converting to big endian is not necessary here, as reference target is encoded little endian
    field current_target = pack128([...[false; 96], ...e[64..96]]);
    valid = valid == true && current_target == reference_target ? true : false;
    bool[256] preimage1 = [...a, ...b];
    bool[256] preimage2 = [...c, ...d];
    bool[256] preimage3 = [...[...e, true], ...[false; 127]];
    bool[256] dummy = [...[false; 246], ...[true, false, true, false, false, false, false, false, false, false]]; //second array indicates length of preimage = 640bit

    u32[8] intermediary = sha256for1024(bool_to_u32(preimage1), bool_to_u32(preimage2), bool_to_u32(preimage3), bool_to_u32(dummy));
    
    u32[8] r = sha256only(u32_to_bool(intermediary));
    bool[256] rbool = u32_to_bool(r);

    field target = packTarget(toBigEndian32bit(e[64..96]));

    valid = valid == true && target > pack128(toBigEndian128bit(u32_to_bool_128(r[4..8]))) ? true : false;

return [valid, ...rbool];
}"""

    main_block = []
    main_block.append("\n\ndef main(field first_block_epoch, field[2] prev_block_hash, private field[{n_intermediate}][5] intermediate_blocks, field[5] final_block) -> (bool[2],field[4],field){{".format(n_intermediate=(n_blocks-1)))
    main_block.append("""
    bool[128] unpacked_raw_target = unpack128(first_block_epoch);
    // converting to big endian is not necessary here, as it is compared to a little endian encoding
    // it is not used for calculations
    field reference_target = pack128([...[false; 96], ...unpacked_raw_target[64..96]]);
    bool mut result = true;
    bool[128] bin_prev_block_hash1 = unpack128(prev_block_hash[0]);
    bool[128] bin_prev_block_hash2 = unpack128(prev_block_hash[1]);
    bool[257] block1 = validate_block_header(reference_target, [...bin_prev_block_hash1, ...bin_prev_block_hash2], intermediate_blocks[0]);
    result =  block1[0] == false || result == false ? false : true;""")

    blocks = []
    for i in range (1, n_blocks-1):
            main_block.append("""\t\tbool[257] block{a} = validate_block_header(reference_target, block{b}[1..257], intermediate_blocks[{b}]);
    result = block{a}[0] == false || result == false ? false : true;""".format(a=i+1,b=i))
            blocks.append('block' + str(i) + '[1..257]')
        
    blocks.append('block' + str(n_blocks-1) + '[1..257]')
    blocks.append('block' + str(n_blocks) + '[1..257]')

    main_block.append("""
    bool[128] e = unpack128(final_block[4]);
    bool[257] block{n_final_block} = validate_block_header(pack128([...[false; 96], ...e[64..96]]), block{n_prev_block}[1..257], final_block);
    result = block{n_final_block}[0] == false || result == false ? false : true;
    assert (result == true);

    //SEPEHR: 0-32 version, 32-288 priv block hash, 288-544 merkle root, 544-576 timestamp([4][32-64]), 576-608 target([4][64-96]) and 608-640 nonce([4][96-128])
    (bool,field) target_is_valid = validate_target(first_block_epoch, intermediate_blocks[{n_enc_target}][4], final_block[4]);

    field[2] merkle_root = compute_merkle_root([{blocks}]);
    field[2] final_block_hash = [pack128(block{n_final_block}[1..129]), pack128(block{n_final_block}[129..257])];
    //assert(target_is_valid.0 == true);
    return ([result,target_is_valid.0], [...final_block_hash, ...merkle_root], target_is_valid.1);

}}""".format(n_final_block=n_blocks, n_prev_block=n_blocks-1, n_enc_target=n_blocks-2, blocks=','.join(blocks)))

    return static_code + "\n".join(main_block)

