#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only
"""Inspect two local uncompressed newc ramdisks; does not unpack/execute a boot."""
import argparse
import hashlib
import json
from pathlib import Path


def entries(path):
    data, offset, result = path.read_bytes(), 0, {}
    while offset + 110 <= len(data):
        if data[offset:offset+6] not in (b'070701', b'070702'):
            raise ValueError('Unsupported CPIO header')
        values = [int(data[offset+6+i*8:offset+14+i*8], 16) for i in range(13)]
        size, name_size = values[6], values[11]
        name_end = offset + 110 + name_size
        if name_size < 1 or name_end > len(data) or data[name_end-1] != 0:
            raise ValueError('Truncated CPIO name')
        name = data[offset+110:name_end-1].decode('utf-8')
        begin = (name_end + 3) & ~3
        if begin + size > len(data):
            raise ValueError('Truncated CPIO payload')
        if name == 'TRAILER!!!':
            return result
        if name in result:
            raise ValueError('Duplicate CPIO entry')
        result[name] = {'mode': values[1], 'uid': values[2], 'gid': values[3], 'nlink': values[4], 'mtime': values[5], 'devmajor': values[7], 'devminor': values[8], 'rdevmajor': values[9], 'rdevminor': values[10], 'sha256': hashlib.sha256(data[begin:begin+size]).hexdigest()}
        offset = (begin + size + 3) & ~3
    raise ValueError('Missing CPIO trailer')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('before', type=Path)
    parser.add_argument('after', type=Path)
    args = parser.parse_args()
    before, after = entries(args.before), entries(args.after)
    missing = sorted(set(before) - set(after))
    changed = sorted(name for name in before.keys() & after.keys() if before[name] != after[name])
    added = sorted(set(after) - set(before))
    print(json.dumps({'originalEntries': len(before), 'missing': missing, 'changed': changed, 'added': added, 'originalEntriesPreserved': not missing and not changed, 'bootOrHardwareValidated': False}, indent=2))
    if missing or changed:
        raise SystemExit(1)


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as error:
        raise SystemExit(f'Error: {error}') from error
