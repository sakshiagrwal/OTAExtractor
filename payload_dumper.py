from collections import deque
from io import BytesIO
import hashlib
import lzma
import bz2
import struct
import sys
import update_metadata_pb2 as um

def u32(x):
    return struct.unpack_from('>I', x)[0]

def u64(x):
    return struct.unpack_from('>Q', x)[0]

def verify_contiguous(exts):
    blocks = 0
    ext_deque = deque(exts)

    while ext_deque:
        ext = ext_deque.popleft()
        if ext.start_block != blocks:
            return False

        blocks += ext.num_blocks

    return True

def data_for_op(op):
    data = p.read(op.data_length)

    assert hashlib.sha256(data).digest() == op.data_sha256_hash, 'operation data hash mismatch'

    if op.type == op.REPLACE_XZ:
        dec = lzma.LZMADecompressor()
        data = dec.decompress(data) 
    elif op.type == op.REPLACE_BZ:
        dec = bz2.BZ2Decompressor()
        data = dec.decompress(data) 

    return data

def dump_part(part):
    print(part.partition_name)

    out_file = open('%s.img' % part.partition_name, 'wb')
    h = hashlib.sha256()
    data = bytearray()

    for op in part.operations:
        data += data_for_op(op)
        h.update(data)

    assert h.digest() == part.new_partition_info.hash, 'partition hash mismatch'
    out_file.write(data)

supported_op_types = {op.REPLACE, op.REPLACE_BZ, op.REPLACE_XZ}

with open(sys.argv[1], 'rb') as f:
    magic = f.read(4)
    assert magic == b'CrAU'

    file_format_version = u64(f.read(8))
    assert file_format_version == 2

    manifest_size = u64(f.read(8))

    metadata_signature_size = 0

    if file_format_version > 1:
        metadata_signature_size = u32(f.read(4))

    manifest = f.read(manifest_size)
    metadata_signature = f.read(metadata_signature_size)

    data_offset = f.tell()

p = BytesIO(f.read())

dam = um.DeltaArchiveManifest()
dam.ParseFromString(manifest)

for part in dam.partitions:
    for op in part.operations:
        assert op.type in supported_op_types, 'unsupported op'

    extents = (op.dst_extents for part in dam.partitions for op in part.operations)
    assert verify_contiguous(extents), '
