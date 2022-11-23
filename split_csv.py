"""Split a CSV file into multiple chunks."""

import os
import sys

from settings import settings

SOURCE_FILE = settings.csv_options['file']
CHUNK_FILE_PREFIX = settings.csv_options['chunck_prefix']
CHUNK_DEST_DIR = settings.csv_options['chunk_dir']
LINES_PER_CHUNK = settings.csv_options['lines_per_chunk']
DELETE_CSV_AFTER_SPLIT = settings.delete_csv_after_split

def main(source_file, dest_dir, chunk_prefix, lines_per_chunk):
    try:
        split_csv(source_file, dest_dir, chunk_prefix, lines_per_chunk)
    except Exception as error:
        sys.exit(f'Error splitting CSV file: \n\n{error}')
    if DELETE_CSV_AFTER_SPLIT:
        print(f'Deleting original file: {source_file}...')
        os.remove(source_file)


def split_csv(source_file, dest_dir, chunk_prefix, lines_per_chunk):
    """Split the source file in chunks and write the chunks to 
    destination directory.
    """
    start_num = get_start_number(dest_dir, chunk_prefix)
    with open(source_file, 'rt', encoding='utf8') as f:
        for file_num, chunk in enumerate(
            read_chunck(f, lines_per_chunk), start=start_num):
            dest_file = dest_dir / f'{chunk_prefix}{file_num:03d}.csv'
            print(f'Writing to file {dest_file}...')
            dest_file.write_text(chunk, encoding='utf8')


def read_chunck(file, number_of_lines):
    """Yield the next chunk of lines from file."""
    chunk = []
    for line in file:
        chunk.append(line)
        if len(chunk) == number_of_lines:
            yield ''.join(chunk)
            chunk = []
    else:
        yield ''.join(chunk)  


def get_start_number(dest_dir, chunk_prefix):
    """Return the first free chunk number. Existing chunks are left
    untouched.
    """
    max_num = 0
    for d in dest_dir.iterdir():
        if d.stem.startswith(chunk_prefix):
            chunk_num = int(d.stem.replace(chunk_prefix, ''))
            if chunk_num > max_num:
                max_num = chunk_num
    return max_num + 1
    

if __name__ == '__main__':
    main(
        SOURCE_FILE,
        CHUNK_DEST_DIR,
        CHUNK_FILE_PREFIX,
        LINES_PER_CHUNK
    )
    