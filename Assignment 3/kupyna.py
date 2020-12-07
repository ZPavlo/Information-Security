import struct
from functools import reduce

import numpy as np

_mds_matrix = [
    [0x01, 0x01, 0x05, 0x01, 0x08, 0x06, 0x07, 0x04],
    [0x04, 0x01, 0x01, 0x05, 0x01, 0x08, 0x06, 0x07],
    [0x07, 0x04, 0x01, 0x01, 0x05, 0x01, 0x08, 0x06],
    [0x06, 0x07, 0x04, 0x01, 0x01, 0x05, 0x01, 0x08],
    [0x08, 0x06, 0x07, 0x04, 0x01, 0x01, 0x05, 0x01],
    [0x01, 0x08, 0x06, 0x07, 0x04, 0x01, 0x01, 0x05],
    [0x05, 0x01, 0x08, 0x06, 0x07, 0x04, 0x01, 0x01],
    [0x01, 0x05, 0x01, 0x08, 0x06, 0x07, 0x04, 0x01],
]

_SBoxes = [
    [
        0xa8, 0x43, 0x5f, 0x06, 0x6b, 0x75, 0x6c, 0x59, 0x71, 0xdf, 0x87, 0x95, 0x17, 0xf0, 0xd8, 0x09,
        0x6d, 0xf3, 0x1d, 0xcb, 0xc9, 0x4d, 0x2c, 0xaf, 0x79, 0xe0, 0x97, 0xfd, 0x6f, 0x4b, 0x45, 0x39,
        0x3e, 0xdd, 0xa3, 0x4f, 0xb4, 0xb6, 0x9a, 0x0e, 0x1f, 0xbf, 0x15, 0xe1, 0x49, 0xd2, 0x93, 0xc6,
        0x92, 0x72, 0x9e, 0x61, 0xd1, 0x63, 0xfa, 0xee, 0xf4, 0x19, 0xd5, 0xad, 0x58, 0xa4, 0xbb, 0xa1,
        0xdc, 0xf2, 0x83, 0x37, 0x42, 0xe4, 0x7a, 0x32, 0x9c, 0xcc, 0xab, 0x4a, 0x8f, 0x6e, 0x04, 0x27,
        0x2e, 0xe7, 0xe2, 0x5a, 0x96, 0x16, 0x23, 0x2b, 0xc2, 0x65, 0x66, 0x0f, 0xbc, 0xa9, 0x47, 0x41,
        0x34, 0x48, 0xfc, 0xb7, 0x6a, 0x88, 0xa5, 0x53, 0x86, 0xf9, 0x5b, 0xdb, 0x38, 0x7b, 0xc3, 0x1e,
        0x22, 0x33, 0x24, 0x28, 0x36, 0xc7, 0xb2, 0x3b, 0x8e, 0x77, 0xba, 0xf5, 0x14, 0x9f, 0x08, 0x55,
        0x9b, 0x4c, 0xfe, 0x60, 0x5c, 0xda, 0x18, 0x46, 0xcd, 0x7d, 0x21, 0xb0, 0x3f, 0x1b, 0x89, 0xff,
        0xeb, 0x84, 0x69, 0x3a, 0x9d, 0xd7, 0xd3, 0x70, 0x67, 0x40, 0xb5, 0xde, 0x5d, 0x30, 0x91, 0xb1,
        0x78, 0x11, 0x01, 0xe5, 0x00, 0x68, 0x98, 0xa0, 0xc5, 0x02, 0xa6, 0x74, 0x2d, 0x0b, 0xa2, 0x76,
        0xb3, 0xbe, 0xce, 0xbd, 0xae, 0xe9, 0x8a, 0x31, 0x1c, 0xec, 0xf1, 0x99, 0x94, 0xaa, 0xf6, 0x26,
        0x2f, 0xef, 0xe8, 0x8c, 0x35, 0x03, 0xd4, 0x7f, 0xfb, 0x05, 0xc1, 0x5e, 0x90, 0x20, 0x3d, 0x82,
        0xf7, 0xea, 0x0a, 0x0d, 0x7e, 0xf8, 0x50, 0x1a, 0xc4, 0x07, 0x57, 0xb8, 0x3c, 0x62, 0xe3, 0xc8,
        0xac, 0x52, 0x64, 0x10, 0xd0, 0xd9, 0x13, 0x0c, 0x12, 0x29, 0x51, 0xb9, 0xcf, 0xd6, 0x73, 0x8d,
        0x81, 0x54, 0xc0, 0xed, 0x4e, 0x44, 0xa7, 0x2a, 0x85, 0x25, 0xe6, 0xca, 0x7c, 0x8b, 0x56, 0x80
    ], [
        0xce, 0xbb, 0xeb, 0x92, 0xea, 0xcb, 0x13, 0xc1, 0xe9, 0x3a, 0xd6, 0xb2, 0xd2, 0x90, 0x17, 0xf8,
        0x42, 0x15, 0x56, 0xb4, 0x65, 0x1c, 0x88, 0x43, 0xc5, 0x5c, 0x36, 0xba, 0xf5, 0x57, 0x67, 0x8d,
        0x31, 0xf6, 0x64, 0x58, 0x9e, 0xf4, 0x22, 0xaa, 0x75, 0x0f, 0x02, 0xb1, 0xdf, 0x6d, 0x73, 0x4d,
        0x7c, 0x26, 0x2e, 0xf7, 0x08, 0x5d, 0x44, 0x3e, 0x9f, 0x14, 0xc8, 0xae, 0x54, 0x10, 0xd8, 0xbc,
        0x1a, 0x6b, 0x69, 0xf3, 0xbd, 0x33, 0xab, 0xfa, 0xd1, 0x9b, 0x68, 0x4e, 0x16, 0x95, 0x91, 0xee,
        0x4c, 0x63, 0x8e, 0x5b, 0xcc, 0x3c, 0x19, 0xa1, 0x81, 0x49, 0x7b, 0xd9, 0x6f, 0x37, 0x60, 0xca,
        0xe7, 0x2b, 0x48, 0xfd, 0x96, 0x45, 0xfc, 0x41, 0x12, 0x0d, 0x79, 0xe5, 0x89, 0x8c, 0xe3, 0x20,
        0x30, 0xdc, 0xb7, 0x6c, 0x4a, 0xb5, 0x3f, 0x97, 0xd4, 0x62, 0x2d, 0x06, 0xa4, 0xa5, 0x83, 0x5f,
        0x2a, 0xda, 0xc9, 0x00, 0x7e, 0xa2, 0x55, 0xbf, 0x11, 0xd5, 0x9c, 0xcf, 0x0e, 0x0a, 0x3d, 0x51,
        0x7d, 0x93, 0x1b, 0xfe, 0xc4, 0x47, 0x09, 0x86, 0x0b, 0x8f, 0x9d, 0x6a, 0x07, 0xb9, 0xb0, 0x98,
        0x18, 0x32, 0x71, 0x4b, 0xef, 0x3b, 0x70, 0xa0, 0xe4, 0x40, 0xff, 0xc3, 0xa9, 0xe6, 0x78, 0xf9,
        0x8b, 0x46, 0x80, 0x1e, 0x38, 0xe1, 0xb8, 0xa8, 0xe0, 0x0c, 0x23, 0x76, 0x1d, 0x25, 0x24, 0x05,
        0xf1, 0x6e, 0x94, 0x28, 0x9a, 0x84, 0xe8, 0xa3, 0x4f, 0x77, 0xd3, 0x85, 0xe2, 0x52, 0xf2, 0x82,
        0x50, 0x7a, 0x2f, 0x74, 0x53, 0xb3, 0x61, 0xaf, 0x39, 0x35, 0xde, 0xcd, 0x1f, 0x99, 0xac, 0xad,
        0x72, 0x2c, 0xdd, 0xd0, 0x87, 0xbe, 0x5e, 0xa6, 0xec, 0x04, 0xc6, 0x03, 0x34, 0xfb, 0xdb, 0x59,
        0xb6, 0xc2, 0x01, 0xf0, 0x5a, 0xed, 0xa7, 0x66, 0x21, 0x7f, 0x8a, 0x27, 0xc7, 0xc0, 0x29, 0xd7
    ], [
        0x93, 0xd9, 0x9a, 0xb5, 0x98, 0x22, 0x45, 0xfc, 0xba, 0x6a, 0xdf, 0x02, 0x9f, 0xdc, 0x51, 0x59,
        0x4a, 0x17, 0x2b, 0xc2, 0x94, 0xf4, 0xbb, 0xa3, 0x62, 0xe4, 0x71, 0xd4, 0xcd, 0x70, 0x16, 0xe1,
        0x49, 0x3c, 0xc0, 0xd8, 0x5c, 0x9b, 0xad, 0x85, 0x53, 0xa1, 0x7a, 0xc8, 0x2d, 0xe0, 0xd1, 0x72,
        0xa6, 0x2c, 0xc4, 0xe3, 0x76, 0x78, 0xb7, 0xb4, 0x09, 0x3b, 0x0e, 0x41, 0x4c, 0xde, 0xb2, 0x90,
        0x25, 0xa5, 0xd7, 0x03, 0x11, 0x00, 0xc3, 0x2e, 0x92, 0xef, 0x4e, 0x12, 0x9d, 0x7d, 0xcb, 0x35,
        0x10, 0xd5, 0x4f, 0x9e, 0x4d, 0xa9, 0x55, 0xc6, 0xd0, 0x7b, 0x18, 0x97, 0xd3, 0x36, 0xe6, 0x48,
        0x56, 0x81, 0x8f, 0x77, 0xcc, 0x9c, 0xb9, 0xe2, 0xac, 0xb8, 0x2f, 0x15, 0xa4, 0x7c, 0xda, 0x38,
        0x1e, 0x0b, 0x05, 0xd6, 0x14, 0x6e, 0x6c, 0x7e, 0x66, 0xfd, 0xb1, 0xe5, 0x60, 0xaf, 0x5e, 0x33,
        0x87, 0xc9, 0xf0, 0x5d, 0x6d, 0x3f, 0x88, 0x8d, 0xc7, 0xf7, 0x1d, 0xe9, 0xec, 0xed, 0x80, 0x29,
        0x27, 0xcf, 0x99, 0xa8, 0x50, 0x0f, 0x37, 0x24, 0x28, 0x30, 0x95, 0xd2, 0x3e, 0x5b, 0x40, 0x83,
        0xb3, 0x69, 0x57, 0x1f, 0x07, 0x1c, 0x8a, 0xbc, 0x20, 0xeb, 0xce, 0x8e, 0xab, 0xee, 0x31, 0xa2,
        0x73, 0xf9, 0xca, 0x3a, 0x1a, 0xfb, 0x0d, 0xc1, 0xfe, 0xfa, 0xf2, 0x6f, 0xbd, 0x96, 0xdd, 0x43,
        0x52, 0xb6, 0x08, 0xf3, 0xae, 0xbe, 0x19, 0x89, 0x32, 0x26, 0xb0, 0xea, 0x4b, 0x64, 0x84, 0x82,
        0x6b, 0xf5, 0x79, 0xbf, 0x01, 0x5f, 0x75, 0x63, 0x1b, 0x23, 0x3d, 0x68, 0x2a, 0x65, 0xe8, 0x91,
        0xf6, 0xff, 0x13, 0x58, 0xf1, 0x47, 0x0a, 0x7f, 0xc5, 0xa7, 0xe7, 0x61, 0x5a, 0x06, 0x46, 0x44,
        0x42, 0x04, 0xa0, 0xdb, 0x39, 0x86, 0x54, 0xaa, 0x8c, 0x34, 0x21, 0x8b, 0xf8, 0x0c, 0x74, 0x67
    ], [
        0x68, 0x8d, 0xca, 0x4d, 0x73, 0x4b, 0x4e, 0x2a, 0xd4, 0x52, 0x26, 0xb3, 0x54, 0x1e, 0x19, 0x1f,
        0x22, 0x03, 0x46, 0x3d, 0x2d, 0x4a, 0x53, 0x83, 0x13, 0x8a, 0xb7, 0xd5, 0x25, 0x79, 0xf5, 0xbd,
        0x58, 0x2f, 0x0d, 0x02, 0xed, 0x51, 0x9e, 0x11, 0xf2, 0x3e, 0x55, 0x5e, 0xd1, 0x16, 0x3c, 0x66,
        0x70, 0x5d, 0xf3, 0x45, 0x40, 0xcc, 0xe8, 0x94, 0x56, 0x08, 0xce, 0x1a, 0x3a, 0xd2, 0xe1, 0xdf,
        0xb5, 0x38, 0x6e, 0x0e, 0xe5, 0xf4, 0xf9, 0x86, 0xe9, 0x4f, 0xd6, 0x85, 0x23, 0xcf, 0x32, 0x99,
        0x31, 0x14, 0xae, 0xee, 0xc8, 0x48, 0xd3, 0x30, 0xa1, 0x92, 0x41, 0xb1, 0x18, 0xc4, 0x2c, 0x71,
        0x72, 0x44, 0x15, 0xfd, 0x37, 0xbe, 0x5f, 0xaa, 0x9b, 0x88, 0xd8, 0xab, 0x89, 0x9c, 0xfa, 0x60,
        0xea, 0xbc, 0x62, 0x0c, 0x24, 0xa6, 0xa8, 0xec, 0x67, 0x20, 0xdb, 0x7c, 0x28, 0xdd, 0xac, 0x5b,
        0x34, 0x7e, 0x10, 0xf1, 0x7b, 0x8f, 0x63, 0xa0, 0x05, 0x9a, 0x43, 0x77, 0x21, 0xbf, 0x27, 0x09,
        0xc3, 0x9f, 0xb6, 0xd7, 0x29, 0xc2, 0xeb, 0xc0, 0xa4, 0x8b, 0x8c, 0x1d, 0xfb, 0xff, 0xc1, 0xb2,
        0x97, 0x2e, 0xf8, 0x65, 0xf6, 0x75, 0x07, 0x04, 0x49, 0x33, 0xe4, 0xd9, 0xb9, 0xd0, 0x42, 0xc7,
        0x6c, 0x90, 0x00, 0x8e, 0x6f, 0x50, 0x01, 0xc5, 0xda, 0x47, 0x3f, 0xcd, 0x69, 0xa2, 0xe2, 0x7a,
        0xa7, 0xc6, 0x93, 0x0f, 0x0a, 0x06, 0xe6, 0x2b, 0x96, 0xa3, 0x1c, 0xaf, 0x6a, 0x12, 0x84, 0x39,
        0xe7, 0xb0, 0x82, 0xf7, 0xfe, 0x9d, 0x87, 0x5c, 0x81, 0x35, 0xde, 0xb4, 0xa5, 0xfc, 0x80, 0xef,
        0xcb, 0xbb, 0x6b, 0x76, 0xba, 0x5a, 0x7d, 0x78, 0x0b, 0x95, 0xe3, 0xad, 0x74, 0x98, 0x3b, 0x36,
        0x64, 0x6d, 0xdc, 0xf0, 0x59, 0xa9, 0x4c, 0x17, 0x7f, 0x91, 0xb8, 0xc9, 0x57, 0x1b, 0xe0, 0x61
    ]
]


def _multiply_gf(x, y):
    r = 0
    for i in range(8):
        if (y & 0x1) == 1:
            r ^= x
        hbit = x & 0x80
        x <<= 1
        if hbit == 0x80:
            x ^= 0x011d
        y >>= 1
    return r


_mult_table = [[0 for j in range(256)] for i in range(256)]
for i in range(256):
    for j in range(256):
        _mult_table[i][j] = _multiply_gf(np.uint8(i), np.uint8(j))


def _add_round_constant_p(state, round, ctx: dict):
    for i in range(ctx["columns"]):
        state[i][0] ^= (i * 0x10) ^ round


def _add_round_constant_q(state, round, ctx: dict):
    s = [struct.unpack("Q", s)[0] for s in state]
    for j in range(ctx["columns"]):
        w = 0x00F0F0F0F0F0F0F3 ^ ((((ctx["columns"] - j - 1) * 0x10) ^ round) << (7 * 8))
        s[j] = (s[j] + w) % (1 << 64)
    for i, s_i in enumerate(s):
        state[i] = bytearray(struct.pack("Q", s_i))


def _sub_bytes(state, ctx: dict):
    for i in range(8):
        for j in range(ctx["columns"]):
            state[j][i] = _SBoxes[i % 4][state[j][i]]


def _shift_bytes(state, ctx: dict):
    temp = [None] * ctx["columns"]
    for shift in range(7):
        for j in range(ctx["columns"]):
            temp[(j + shift) % ctx["columns"]] = state[j][shift]
        for j in range(ctx["columns"]):
            state[j][shift] = temp[j]

    if ctx["columns"] == 16:
        shift = 11
    else:
        shift += 1

    for j in range(ctx["columns"]):
        temp[(j + shift) % ctx["columns"]] = state[j][7]
    for j in range(ctx["columns"]):
        state[j][7] = temp[j]


def _mix_columns(state, ctx: dict):
    temp = [0] * 8
    for col in range(ctx["columns"]):
        for row in range(7, -1, -1):
            product = 0
            for b in range(7, -1, -1):
                product ^= _mult_table[state[col][b]][_mds_matrix[row][b]]
            temp[row] = product
        for i in range(8):
            state[col][i] = temp[i]


def _P(state, ctx: dict):
    for i in range(ctx["rounds"]):
        _add_round_constant_p(state, i, ctx)
        _sub_bytes(state, ctx)
        _shift_bytes(state, ctx)
        _mix_columns(state, ctx)


def _Q(state, ctx: dict):
    for i in range(ctx["rounds"]):
        _add_round_constant_q(state, i, ctx)
        _sub_bytes(state, ctx)
        _shift_bytes(state, ctx)
        _mix_columns(state, ctx)


def _padding(message: bytearray, ctx: dict):
    nblocks = len(message) // ctx["nbytes"]
    pad_nbytes = len(message) - (nblocks * ctx["nbytes"])
    data_nbytes = len(message) - pad_nbytes

    zero_nbytes = ((-len(message) * 8 - 97) % (ctx["nbytes"] * 8)) // 8
    padding = message[data_nbytes:data_nbytes + pad_nbytes].copy() + bytearray([0x80]) + bytearray(zero_nbytes) + \
              bytearray([((len(message) * 8) >> (i * 8)) & 0xFF if i < 8 else 0 for i in range(96 // 8)])

    ctx["data_nbytes"] = data_nbytes
    ctx["pad_nbytes"] = len(padding)
    ctx["padding"] = [padding[i:i + 8] for i in range(0, len(padding), 8)]


def _digest(message: bytearray, ctx: dict):
    message = [message[i:i + 8] for i in range(0, len(message), 8)]
    for b in range(ctx["data_nbytes"] // ctx["nbytes"]):
        temp1 = [bytearray([d ^ s for d, s in zip(data_row, state_row)]) for data_row, state_row in
                 zip(message[ctx["nbytes"] * b // 8:], ctx["state"])]
        temp2 = [bytearray([p for p in pad_row]) for pad_row in
                 message[ctx["nbytes"] * b // 8:ctx["nbytes"] * (b + 1) // 8]]
        _P(temp1, ctx)
        _Q(temp2, ctx)
        ctx["state"] = [bytearray([sc ^ c1 ^ c2 for sc, c1, c2 in zip(srow, row1, row2)]) for srow, row1, row2 in
                        zip(ctx["state"], temp1, temp2)]

    for b in range(ctx["pad_nbytes"] // ctx["nbytes"]):
        temp1 = [bytearray([p ^ s for p, s in zip(pad_row, state_row)]) for pad_row, state_row in
                 zip(ctx["padding"][ctx["nbytes"] * b // 8:], ctx["state"])]
        temp2 = [bytearray([p for p in pad_row]) for pad_row in
                 ctx["padding"][ctx["nbytes"] * b // 8:ctx["nbytes"] * (b + 1) // 8]]
        _P(temp1, ctx)
        _Q(temp2, ctx)
        ctx["state"] = [bytearray([sc ^ c1 ^ c2 for sc, c1, c2 in zip(srow, row1, row2)]) for srow, row1, row2 in
                        zip(ctx["state"], temp1, temp2)]


def _output_transformation(ctx: dict):
    temp = [row.copy() for row in ctx["state"]]
    _P(temp, ctx)
    ctx["state"] = [bytearray([t ^ s for t, s in zip(temp_row, state_row)]) for temp_row, state_row in
                    zip(temp, ctx["state"])]
    state = reduce(lambda x, y: x + y, ctx["state"])
    return state[-ctx["hash_nbits"] // 8:]


def kupyna(message: bytearray, hash_nbits) -> bytearray:
    ctx = {
        "rounds": None,
        "columns": None,
        "nbytes": None,
        "state": None,
        "data_nbytes": None,
        "padding": None,
        "pad_nbytes": None,
        "hash_nbits": hash_nbits
    }

    assert ctx["hash_nbits"] % 8 == 0 and ctx["hash_nbits"] <= 512

    if ctx["hash_nbits"] <= 256:
        ctx["rounds"], ctx["columns"], ctx["nbytes"] = (10, 8, 8 * 8)
    else:
        ctx["rounds"], ctx["columns"], ctx["nbytes"] = (14, 16, 8 * 16)

    ctx["state"] = [bytearray(8) for i in range(0, ctx["nbytes"], 8)]
    ctx["state"][0][0] = ctx["nbytes"]

    _padding(message, ctx)
    _digest(message, ctx)
    return _output_transformation(ctx)


if __name__ == '__main__':
    test_8 = bytearray([0xFF])
    test_33 = bytearray([0x00, 0x00, 0xFF, 0x00, 0x00])

    test = bytearray([
        0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
        0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F,
        0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F,
        0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0x3E, 0x3F,
        0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4A, 0x4B, 0x4C, 0x4D, 0x4E, 0x4F,
        0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5A, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F,
        0x60, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6A, 0x6B, 0x6C, 0x6D, 0x6E, 0x6F,
        0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7A, 0x7B, 0x7C, 0x7D, 0x7E, 0x7F,
        0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x8A, 0x8B, 0x8C, 0x8D, 0x8E, 0x8F,
        0x90, 0x91, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9A, 0x9B, 0x9C, 0x9D, 0x9E, 0x9F,
        0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5, 0xA6, 0xA7, 0xA8, 0xA9, 0xAA, 0xAB, 0xAC, 0xAD, 0xAE, 0xAF,
        0xB0, 0xB1, 0xB2, 0xB3, 0xB4, 0xB5, 0xB6, 0xB7, 0xB8, 0xB9, 0xBA, 0xBB, 0xBC, 0xBD, 0xBE, 0xBF,
        0xC0, 0xC1, 0xC2, 0xC3, 0xC4, 0xC5, 0xC6, 0xC7, 0xC8, 0xC9, 0xCA, 0xCB, 0xCC, 0xCD, 0xCE, 0xCF,
        0xD0, 0xD1, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7, 0xD8, 0xD9, 0xDA, 0xDB, 0xDC, 0xDD, 0xDE, 0xDF,
        0xE0, 0xE1, 0xE2, 0xE3, 0xE4, 0xE5, 0xE6, 0xE7, 0xE8, 0xE9, 0xEA, 0xEB, 0xEC, 0xED, 0xEE, 0xEF,
        0xF0, 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7, 0xF8, 0xF9, 0xFA, 0xFB, 0xFC, 0xFD, 0xFE, 0xFF])

    hash_256_1 = bytearray([
        0x08, 0xF4, 0xEE, 0x6F, 0x1B, 0xE6, 0x90, 0x3B, 0x32, 0x4C, 0x4E, 0x27, 0x99, 0x0C, 0xB2, 0x4E,
        0xF6, 0x9D, 0xD5, 0x8D, 0xBE, 0x84, 0x81, 0x3E, 0xE0, 0xA5, 0x2F, 0x66, 0x31, 0x23, 0x98, 0x75
    ])
    hash_256_2 = bytearray([
        0x0A, 0x94, 0x74, 0xE6, 0x45, 0xA7, 0xD2, 0x5E, 0x25, 0x5E, 0x9E, 0x89, 0xFF, 0xF4, 0x2E, 0xC7,
        0xEB, 0x31, 0x34, 0x90, 0x07, 0x05, 0x92, 0x84, 0xF0, 0xB1, 0x82, 0xE4, 0x52, 0xBD, 0xA8, 0x82
    ])
    hash_256_3 = bytearray([
        0xD3, 0x05, 0xA3, 0x2B, 0x96, 0x3D, 0x14, 0x9D, 0xC7, 0x65, 0xF6, 0x85, 0x94, 0x50, 0x5D, 0x40,
        0x77, 0x02, 0x4F, 0x83, 0x6C, 0x1B, 0xF0, 0x38, 0x06, 0xE1, 0x62, 0x4C, 0xE1, 0x76, 0xC0, 0x8F
    ])
    hash_256_4 = bytearray([
        0xEA, 0x76, 0x77, 0xCA, 0x45, 0x26, 0x55, 0x56, 0x80, 0x44, 0x1C, 0x11, 0x79, 0x82, 0xEA, 0x14,
        0x05, 0x9E, 0xA6, 0xD0, 0xD7, 0x12, 0x4D, 0x6E, 0xCD, 0xB3, 0xDE, 0xEC, 0x49, 0xE8, 0x90, 0xF4
    ])
    hash_256_5 = bytearray([
        0x10, 0x75, 0xC8, 0xB0, 0xCB, 0x91, 0x0F, 0x11, 0x6B, 0xDA, 0x5F, 0xA1, 0xF1, 0x9C, 0x29, 0xCF,
        0x8E, 0xCC, 0x75, 0xCA, 0xFF, 0x72, 0x08, 0xBA, 0x29, 0x94, 0xB6, 0x8F, 0xC5, 0x6E, 0x8D, 0x16
    ])
    hash_256_6 = bytearray([
        0xCD, 0x51, 0x01, 0xD1, 0xCC, 0xDF, 0x0D, 0x1D, 0x1F, 0x4A, 0xDA, 0x56, 0xE8, 0x88, 0xCD, 0x72,
        0x4C, 0xA1, 0xA0, 0x83, 0x8A, 0x35, 0x21, 0xE7, 0x13, 0x1D, 0x4F, 0xB7, 0x8D, 0x0F, 0x5E, 0xB6
    ])
    hash_256_7 = bytearray([
        0x87, 0x5C, 0x00, 0x23, 0xDA, 0xA0, 0xC0, 0x77, 0x80, 0x9F, 0xDD, 0x6A, 0x96, 0x72, 0xB4, 0x9E,
        0x03, 0x90, 0x3B, 0xFF, 0x98, 0xEB, 0xE4, 0x87, 0x40, 0xAE, 0x99, 0x8C, 0x7B, 0xE3, 0x85, 0x1E
    ])
    hash_256_8 = bytearray([
        0x42, 0x37, 0xD7, 0xDE, 0x1A, 0x00, 0xC4, 0xCC, 0x80, 0x37, 0xED, 0xE9, 0xC5, 0x4B, 0xA6, 0x0D,
        0x1C, 0x70, 0x5C, 0xD1, 0x49, 0x5D, 0xE1, 0x9E, 0x52, 0x45, 0xBF, 0x35, 0x09, 0xDB, 0x59, 0xCE
    ])
    hash_48 = bytearray([
        0x2F, 0x66, 0x31, 0x23, 0x98, 0x75
    ])
    hash_512_1 = bytearray([
        0x38, 0x13, 0xE2, 0x10, 0x91, 0x18, 0xCD, 0xFB, 0x5A, 0x6D, 0x5E, 0x72, 0xF7, 0x20, 0x8D, 0xCC,
        0xC8, 0x0A, 0x2D, 0xFB, 0x3A, 0xFD, 0xFB, 0x02, 0xF4, 0x69, 0x92, 0xB5, 0xED, 0xBE, 0x53, 0x6B,
        0x35, 0x60, 0xDD, 0x1D, 0x7E, 0x29, 0xC6, 0xF5, 0x39, 0x78, 0xAF, 0x58, 0xB4, 0x44, 0xE3, 0x7B,
        0xA6, 0x85, 0xC0, 0xDD, 0x91, 0x05, 0x33, 0xBA, 0x5D, 0x78, 0xEF, 0xFF, 0xC1, 0x3D, 0xE6, 0x2A
    ])
    hash_512_2 = bytearray([
        0x76, 0xED, 0x1A, 0xC2, 0x8B, 0x1D, 0x01, 0x43, 0x01, 0x3F, 0xFA, 0x87, 0x21, 0x3B, 0x40, 0x90,
        0xB3, 0x56, 0x44, 0x12, 0x63, 0xC1, 0x3E, 0x03, 0xFA, 0x06, 0x0A, 0x8C, 0xAD, 0xA3, 0x2B, 0x97,
        0x96, 0x35, 0x65, 0x7F, 0x25, 0x6B, 0x15, 0xD5, 0xFC, 0xA4, 0xA1, 0x74, 0xDE, 0x02, 0x9F, 0x0B,
        0x1B, 0x43, 0x87, 0xC8, 0x78, 0xFC, 0xC1, 0xC0, 0x0E, 0x87, 0x05, 0xD7, 0x83, 0xFD, 0x7F, 0xFE
    ])
    hash_512_3 = bytearray([
        0x0D, 0xD0, 0x3D, 0x73, 0x50, 0xC4, 0x09, 0xCB, 0x3C, 0x29, 0xC2, 0x58, 0x93, 0xA0, 0x72, 0x4F,
        0x6B, 0x13, 0x3F, 0xA8, 0xB9, 0xEB, 0x90, 0xA6, 0x4D, 0x1A, 0x8F, 0xA9, 0x3B, 0x56, 0x55, 0x66,
        0x11, 0xEB, 0x18, 0x7D, 0x71, 0x5A, 0x95, 0x6B, 0x10, 0x7E, 0x3B, 0xFC, 0x76, 0x48, 0x22, 0x98,
        0x13, 0x3A, 0x9C, 0xE8, 0xCB, 0xC0, 0xBD, 0x5E, 0x14, 0x36, 0xA5, 0xB1, 0x97, 0x28, 0x4F, 0x7E
    ])
    hash_512_4 = bytearray([
        0x87, 0x1B, 0x18, 0xCF, 0x75, 0x4B, 0x72, 0x74, 0x03, 0x07, 0xA9, 0x7B, 0x44, 0x9A, 0xBE, 0xB3,
        0x2B, 0x64, 0x44, 0x4C, 0xC0, 0xD5, 0xA4, 0xD6, 0x58, 0x30, 0xAE, 0x54, 0x56, 0x83, 0x7A, 0x72,
        0xD8, 0x45, 0x8F, 0x12, 0xC8, 0xF0, 0x6C, 0x98, 0xC6, 0x16, 0xAB, 0xE1, 0x18, 0x97, 0xF8, 0x62,
        0x63, 0xB5, 0xCB, 0x77, 0xC4, 0x20, 0xFB, 0x37, 0x53, 0x74, 0xBE, 0xC5, 0x2B, 0x6D, 0x02, 0x92
    ])
    hash_512_5 = bytearray([
        0xB1, 0x89, 0xBF, 0xE9, 0x87, 0xF6, 0x82, 0xF5, 0xF1, 0x67, 0xF0, 0xD7, 0xFA, 0x56, 0x53, 0x30,
        0xE1, 0x26, 0xB6, 0xE5, 0x92, 0xB1, 0xC5, 0x5D, 0x44, 0x29, 0x90, 0x64, 0xEF, 0x95, 0xB1, 0xA5,
        0x7F, 0x3C, 0x2D, 0x0E, 0xCF, 0x17, 0x86, 0x9D, 0x1D, 0x19, 0x9E, 0xBB, 0xD0, 0x2E, 0x88, 0x57,
        0xFB, 0x8A, 0xDD, 0x67, 0xA8, 0xC3, 0x1F, 0x56, 0xCD, 0x82, 0xC0, 0x16, 0xCF, 0x74, 0x31, 0x21
    ])
    hash_512_6 = bytearray([
        0x65, 0x6B, 0x2F, 0x4C, 0xD7, 0x14, 0x62, 0x38, 0x8B, 0x64, 0xA3, 0x70, 0x43, 0xEA, 0x55, 0xDB,
        0xE4, 0x45, 0xD4, 0x52, 0xAE, 0xCD, 0x46, 0xC3, 0x29, 0x83, 0x43, 0x31, 0x4E, 0xF0, 0x40, 0x19,
        0xBC, 0xFA, 0x3F, 0x04, 0x26, 0x5A, 0x98, 0x57, 0xF9, 0x1B, 0xE9, 0x1F, 0xCE, 0x19, 0x70, 0x96,
        0x18, 0x7C, 0xED, 0xA7, 0x8C, 0x9C, 0x1C, 0x02, 0x1C, 0x29, 0x4A, 0x06, 0x89, 0x19, 0x85, 0x38
    ])
    hash_512_7 = bytearray([
        0x2F, 0x3B, 0xBA, 0xC9, 0x8E, 0x87, 0x71, 0xD6, 0xE3, 0xB8, 0xAA, 0x30, 0x15, 0x3A, 0xBC, 0x4D,
        0x0C, 0x29, 0x85, 0xE9, 0x1D, 0xA1, 0xB5, 0x56, 0x8F, 0xD1, 0xBD, 0xD7, 0x05, 0xCC, 0xAB, 0x7E,
        0xE8, 0xD9, 0x5D, 0x2F, 0xC9, 0x8B, 0xFA, 0x53, 0x22, 0xA2, 0x41, 0xE0, 0x9C, 0x89, 0x6B, 0x58,
        0x28, 0x4C, 0x83, 0xF2, 0x48, 0x8C, 0xF9, 0x43, 0xE4, 0xB3, 0xDE, 0x43, 0xE0, 0x5F, 0x0D, 0xEA
    ])
    hash_512_8 = bytearray([
        0x01, 0xB7, 0xBD, 0xA1, 0xDB, 0xA7, 0x7D, 0x73, 0x79, 0xF5, 0x3C, 0x2A, 0x49, 0x8A, 0x39, 0x0D,
        0xE5, 0xE6, 0x88, 0xA1, 0x2B, 0xC7, 0x5F, 0xEE, 0x9E, 0x01, 0x0C, 0xB6, 0xFE, 0xBE, 0xD3, 0xB9,
        0xC7, 0x02, 0x39, 0x31, 0xC7, 0x4A, 0x7B, 0x55, 0x16, 0x8A, 0x15, 0x04, 0x7D, 0x5E, 0x2C, 0xB7,
        0x8A, 0x8B, 0x5C, 0xA2, 0xF7, 0x5E, 0x05, 0xE8, 0x0C, 0xA3, 0x98, 0x03, 0x0E, 0x02, 0xC7, 0xAA
    ])
    hash_304 = bytearray([
        0x0A, 0x8C, 0xAD, 0xA3, 0x2B, 0x97, 0x96, 0x35, 0x65, 0x7F, 0x25, 0x6B, 0x15, 0xD5, 0xFC, 0xA4,
        0xA1, 0x74, 0xDE, 0x02, 0x9F, 0x0B, 0x1B, 0x43, 0x87, 0xC8, 0x78, 0xFC, 0xC1, 0xC0, 0x0E, 0x87,
        0x05, 0xD7, 0x83, 0xFD, 0x7F, 0xFE
    ])
    hash_384_1 = bytearray([
        0xD9, 0x02, 0x16, 0x92, 0xD8, 0x4E, 0x51, 0x75, 0x73, 0x56, 0x54, 0x84, 0x6B, 0xA7, 0x51, 0xE6,
        0xD0, 0xED, 0x0F, 0xAC, 0x36, 0xDF, 0xBC, 0x08, 0x41, 0x28, 0x7D, 0xCB, 0x0B, 0x55, 0x84, 0xC7,
        0x50, 0x16, 0xC3, 0xDE, 0xCC, 0x2A, 0x6E, 0x47, 0xC5, 0x0B, 0x2F, 0x38, 0x11, 0xE3, 0x51, 0xB8
    ])
    hash_384_2 = bytearray([
        0xB0, 0x33, 0x18, 0x47, 0xCB, 0x0F, 0x28, 0xE0, 0xA7, 0xEC, 0xCB, 0xDF, 0x72, 0x38, 0x6F, 0x49,
        0x2B, 0x8A, 0x07, 0xBD, 0x6A, 0xE6, 0xB4, 0xAF, 0x8C, 0x27, 0x9F, 0x1C, 0x1E, 0x8D, 0x77, 0x1C,
        0xD0, 0x33, 0x91, 0x7F, 0xCD, 0xFD, 0x22, 0xEB, 0x20, 0xA0, 0xC4, 0xF6, 0x63, 0xC3, 0x61, 0x1D
    ])
    hash_384_3 = bytearray([
        0x80, 0x1B, 0xA7, 0xAC, 0xEF, 0xFF, 0x77, 0x1F, 0xC3, 0x31, 0x69, 0x05, 0x12, 0xD4, 0x32, 0xEF,
        0x03, 0x18, 0x29, 0xED, 0xF1, 0x70, 0x5B, 0x48, 0x7D, 0x90, 0xB8, 0xA3, 0x33, 0xC2, 0x98, 0x68,
        0xF5, 0x86, 0xB3, 0x77, 0xBE, 0x9C, 0x92, 0xF0, 0x8D, 0x63, 0xF7, 0x92, 0x77, 0xC8, 0x22, 0x21])


    def check(target: bytearray, output: bytearray):
        print("target", target.hex())
        print("output", output.hex())
        assert target == output, "False"
        print("True")
        print("**************************\n")


    check(hash_256_1, kupyna(test[:512 // 8], 256))
    check(hash_256_2, kupyna(test[:1024 // 8], 256))
    check(hash_256_3, kupyna(test[:2048 // 8], 256))
    check(hash_256_4, kupyna(test_8, 256))
    check(hash_256_5, kupyna(test[:760 // 8], 256))
    check(hash_256_6, kupyna(test[:0 // 8], 256))

    check(hash_48, kupyna(test[:512 // 8], 48))

    check(hash_512_1, kupyna(test[:512 // 8], 512))
    check(hash_512_2, kupyna(test[:1024 // 8], 512))
    check(hash_512_3, kupyna(test[:2048 // 8], 512))
    check(hash_512_4, kupyna(test_8, 512))
    check(hash_512_6, kupyna(test[:0 // 8], 512))

    check(hash_304, kupyna(test[:1024 // 8], 304))
    check(hash_384_1, kupyna(test[:760 // 8], 384))
