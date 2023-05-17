import time
import os
import shutil


def file_fmt_chk(file_list):
    """
    Check Citi file requirements

    :param file_list - File list to be checked
    """

    checked_files = {'chk_pass': [], 'chk_fail': []}

    if file_list:
        print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* Checking file format')

        for file in file_list:

            try:
                numeric_blocks = file[:10] + file[11:14] + file[15:18] + file[19:39]  # validating numeric blocks
                hyphen_pos = file[10] + file[14] + file[18]  # validating hyphen position
                extension_pos = file[-4:].lower()  # validating extension

                if numeric_blocks.isnumeric() and hyphen_pos == '---' and extension_pos == '.ret' and len(file) == 43:
                    print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* File {file} PASS in format checking step')
                    checked_files['chk_pass'].append(file)
                else:
                    print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*WARNING* File {file} FAIL in format checking step')
                    checked_files['chk_fail'].append(file)

            except IndexError:
                print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*WARNING* File {file} FAIL in format checking step')
                checked_files['chk_fail'].append(file)

        return checked_files
    else:
        print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* No files to validate')
        return checked_files


def file_move(files, src_dir, dst_dir):
    """
    Move files from a directory

    :param files   - List of files to move
    :param src_dir - Source directory where the files are
    :param dst_dir - Destination directory where the files have to be moved
    """

    try:
        for file in files:
            src_full_path = os.path.join(src_dir, file)

            if src_dir != dst_dir:
                shutil.move(src=src_full_path, dst=dst_dir)
                print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* Moving {file} to {dst_dir}')
            else:
                print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* Source and destination path are identical. '
                                                          f'Operation aborted!')
    except shutil.Error:
        print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* The {file} already exists in {dst_dir}')


def file_copy(files, src_dir, dst_dir):
    """
    Copy files from a directory

    :param files   - A string or a list of string with name of files
    :param src_dir - The source directory where the files are from
    :param dst_dir - The destination directory where the files must be copied
    """

    if isinstance(files, list):
        for file in files:
            src_full_path = os.path.join(src_dir, file)

            shutil.copy(src=src_full_path, dst=dst_dir)
            print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* Coping {file} to {dst_dir}')

    elif isinstance(files, str):
        shutil.copy(src=os.path.join(src_dir, files), dst=dst_dir)
        print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* Coping {files} to {dst_dir}')


def file_delete(files, dir):
    """
    Delete files from a directory

    :param files - A string or a list of string with name of files
    :param dir   - The source directory where the files is from
    """

    if isinstance(files, list):
        for file in files:
            file_full_path = os.path.join(dir, file)

            os.remove(file_full_path)
            print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* Removing {file} from {dir}')

    elif isinstance(files, str):
        os.remove(os.path.join(dir, files))
        print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* Removing {files} from {dir}')


def file_detect_extension(file):
    """
    Detect file extension
    If had a valid extension the function returns the extension
    If had no extension the function returns a string with 'no_extension'

    :param file - The filename or file full-path
    """

    pos = file.rfind('.')
    if pos > -1:
        return file[pos:]
    else:
        return f'no_extension'


def file_in_directory(dir):
    """
    List all files in directory

    :param dir - Path of the local directory

    Returns A list of the directory content
    """
    file_list = list()

    try:
        print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* Listing files in source directory {dir.upper()}')
        files = os.listdir(dir)

        for file in files:
            if os.path.isfile(os.path.join(dir, file)):
                file_list.append(file)

        return file_list

    except FileNotFoundError:
        print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* Directory not found {dir.upper()}')
    except PermissionError:
        print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* You do not have permission to access {dir.upper()}')


def file_compare(src_dir, tgt_dir):
    """
    Checks what files are in source that is not in target directory

    :param src_dir: Source directory
    :param tgt_dir: Target directory

    Returns A list of files that does not exist in target
    """

    try:
        file_list = list()

        src = os.listdir(src_dir)
        tgt = os.listdir(tgt_dir)

        for file in src:
            if file in tgt:
                pass
            else:
                file_list.append(file)

        return file_list

    except FileNotFoundError:
        print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* Directory not found {src_dir.upper()} or {tgt_dir.upper()}')
    except PermissionError:
        print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* You do not have permission to access '
                                                  f'{src_dir.upper()} or {tgt_dir.upper()}')
