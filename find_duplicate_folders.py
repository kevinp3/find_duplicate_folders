
import argparse
import sys
import os
import os.path
import more_itertools
import functools


def acquire_file_data(input_fpath):
    with open(input_fpath) as fp:
        flist = [line.strip().partition(' ') for line in fp if line]
        expanded = [(w[0], *os.path.split(w[2])) for w in flist]
    return expanded

def list_folders(flist):
    folders = sorted({record[1] for record in flist}, key=lambda x: len(x), reverse=True)
    return folders

def record_in_folder(record, folder):
    return record[1] == folder

def partition_flist(folder, flist):
    partition_pred = functools.partial(record_in_folder, folder=folder)
    other_files, folder_files = more_itertools.partition(partition_pred, flist)
    other_files = list(other_files)
    folder_files = list(folder_files)
    assert len(other_files) + len(folder_files) == len(flist)
    return other_files, folder_files

def map_other_files(other_records):
    record_map = {}
    for record in other_records:
        record_map.setdefault(record[0], []).append(record)
    return record_map

def find_dups(record_map, folder_files):
    dup_state = [record_map.get(folder_record[0]) for folder_record in folder_files]
    return dup_state


def main(input_fpath):
    '''From input_fpath, read a summary of fpaths and sha_xx codes.
    '''
    flist = acquire_file_data(input_fpath)
    folders = list_folders(flist)
    for folder in folders:
        other_files, folder_files = partition_flist(folder, flist)
        record_map = map_other_files(other_files)
        folder_files_dups = find_dups(record_map, folder_files)
        if all(folder_files_dups):
            # This means all files in "folder" are also present in some other folder
            # Present results, so user can determine whether to delete folder
            print('Duplicated folder:', folder)
            for src_record, dst_records in zip(folder_files, folder_files_dups):
                print('    ', src_record[:])
                for dst_record in dst_records:
                    print(' '*8, dst_record[1:])




if __name__ == '__main__':
    print(sys.argv)
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', required=True,
                        help='Folder to examine')
    args = parser.parse_args()
    main(args.input_file)

