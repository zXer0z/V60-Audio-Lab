#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only
"""Generate ROM-pinned audio candidates offline. Never connects to a device."""
import argparse
import hashlib
import json
from pathlib import Path


def sha(data):
    return hashlib.sha256(data).hexdigest()


def transform(original, spec):
    if len(original) != spec['inputSize'] or sha(original) != spec['inputSha256']:
        raise ValueError(f"{spec['name']}: unsupported input; nothing will be generated")
    if spec.get('normalizeNewlines'):
        original = original.replace(b'\r\n', b'\n')
    output, cursor = bytearray(), 0
    for edit in spec['edits']:
        offset = edit['offset']
        old, new = bytes.fromhex(edit['beforeHex']), bytes.fromhex(edit['afterHex'])
        if not isinstance(offset, int) or offset < cursor or offset + len(old) > len(original):
            raise ValueError(f"{spec['name']}: invalid or overlapping edit")
        if original[offset:offset + len(old)] != old:
            raise ValueError(f"{spec['name']}: instruction/content precondition failed")
        output.extend(original[cursor:offset]); output.extend(new)
        cursor = offset + len(old)
    output.extend(original[cursor:])
    result = bytes(output)
    if spec.get('normalizeNewlines'):
        if spec['outputNewline'] == 'crlf':
            result = result.replace(b'\n', b'\r\n')
        elif spec['outputNewline'] != 'lf':
            raise ValueError('Unsupported output newline style')
    if len(result) != spec['outputSize'] or sha(result) != spec['outputSha256']:
        raise ValueError(f"{spec['name']}: output verification failed")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-dir', required=True, type=Path)
    parser.add_argument('--output-dir', required=True, type=Path, help='Must not already exist')
    parser.add_argument('--recipe', type=Path, default=Path(__file__).resolve().parents[1] / 'recipes/timelm-dop128-24.json')
    args = parser.parse_args()
    source, destination = args.input_dir.resolve(), args.output_dir.resolve()
    if destination.exists():
        raise ValueError('Output already exists; refusing to overwrite it')
    if destination == source or destination in source.parents or source in destination.parents:
        raise ValueError('Keep inputs and outputs in separate, non-nested directories')
    recipe = json.loads(args.recipe.read_text(encoding='utf-8'))
    if recipe.get('schemaVersion') != 1:
        raise ValueError('Unsupported recipe schema')
    names, candidates = set(), []
    for spec in recipe['files']:
        name = spec['name']
        if not isinstance(name, str) or not name or '/' in name or '\\' in name or ':' in name or name in ('.', '..', 'manifest.json') or name in names:
            raise ValueError('Invalid or duplicate recipe filename')
        names.add(name)
        path = source / name
        if path.is_symlink() or not path.is_file():
            raise ValueError(f'{name}: input must be a regular file')
        candidates.append((spec, transform(path.read_bytes(), spec)))
    # All source hashes and generated candidates are checked before creating output.
    destination.mkdir(parents=True, exist_ok=False)
    for spec, data in candidates:
        with (destination / spec['name']).open('xb') as output:
            output.write(data)
    report = {'recipe': recipe['name'], 'deployed': False, 'files': {spec['name']: sha(data) for spec, data in candidates}}
    (destination / 'manifest.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    print('Offline generation complete. No device was connected or modified.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise SystemExit(f'Error: {error}') from error
