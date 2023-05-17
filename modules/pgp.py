import os
import time
from modules import file_ops


def pgp_decrypt_file(passphrase, encrypted_files, encrypted_files_dir, decrypted_files_dir):
    """
    Decrypts files with PGP encryption

    :param passphrase          - The passphrase needed to decrypt the file
    :param encrypted_files     - The filename or a list of files that you need to decrypt
    :param decrypted_files_dir - The local path where the files will be hosted after decryption
    :param encrypted_files_dir - The local path where the encrypted files are
    """

    if isinstance(encrypted_files, list):
        for file in encrypted_files:

            #  building full path files
            full_path_encrypted = os.path.join(encrypted_files_dir, file)
            full_path_decrypted = os.path.join(decrypted_files_dir, file)

            #  Decrypting files using GnuPG
            os.system('gpg --batch --pinentry-mode=loopback --yes --passphrase ' + passphrase + ' --decrypt -o ' + full_path_decrypted + ' ' + full_path_encrypted)

            #  Logging decrypted files
            print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* decrypting file {full_path_decrypted}')

    elif isinstance(encrypted_files, str):

        #  building full path files
        full_path_encrypted = os.path.join(encrypted_files_dir, encrypted_files)
        full_path_decrypted = os.path.join(decrypted_files_dir, encrypted_files)

        #  Decrypting files using GnuPG
        os.system(
            'gpg --batch --pinentry-mode=loopback --yes --passphrase ' + passphrase + ' --decrypt -o ' + full_path_decrypted + ' ' + full_path_encrypted)

        #  Logging decrypted files
        print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* decrypting file {full_path_decrypted}')

    else:
        #  Logging decrypted files
        print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* Only variables string or list type are supported')


def pgp_encrypt_file(recipient, decrypted_files, decrypted_files_dir, encrypted_files_dir):
    """
    :param recipient           - Name of the certificate recipient
    :param decrypted_files     - Name of the source file that you need to encrypt
    :param decrypted_files_dir - Directory where the source files are
    :param encrypted_files_dir - Directory where the destination encrypted files will be saved
    """
    if isinstance(decrypted_files, list):
        for file in decrypted_files:

            #  Checks the extension of files
            file_extension = file_ops.file_detect_extension(file)

            if file_extension != 'no_extension':

                #  building full path files
                full_path_encrypted = os.path.join(encrypted_files_dir, file.replace(file_extension, '.pgp'))
                full_path_decrypted = os.path.join(decrypted_files_dir, file)

                #  Decrypting files using GnuPG
                os.system('gpg --batch --pinentry-mode=loopback --yes --recipient ' + recipient + ' --encrypt -o ' + full_path_encrypted + ' ' + full_path_decrypted)

                #  Logging decrypted files
                print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* encrypting file {full_path_encrypted}')

            else:
                #  building full path files
                full_path_encrypted = os.path.join(encrypted_files_dir, file)
                full_path_decrypted = os.path.join(decrypted_files_dir, file)

                #  Decrypting files using GnuPG
                os.system(
                    'gpg --batch --pinentry-mode=loopback --yes --recipient ' + recipient + ' --encrypt -o ' + full_path_encrypted + ' ' + full_path_decrypted)

                #  Logging decrypted files
                print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* encrypting file {full_path_encrypted}')

    elif isinstance(decrypted_files, str):

        #  Checks the extension of file
        file_extension = file_ops.file_detect_extension(decrypted_files)

        if file_extension != 'no_extension':

            #  building full path files
            full_path_encrypted = os.path.join(encrypted_files_dir, decrypted_files.replace(file_extension, '.pgp'))
            full_path_decrypted = os.path.join(decrypted_files_dir, decrypted_files)

            #  Decrypting files using GnuPG
            os.system('gpg --batch --pinentry-mode=loopback --yes --recipient ' + recipient + ' --encrypt -o ' + full_path_encrypted + ' ' + full_path_decrypted)

            #  Logging decrypted files
            print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* encrypting file {full_path_encrypted}')

        else:
            #  building full path files
            full_path_encrypted = os.path.join(encrypted_files_dir, decrypted_files)
            full_path_decrypted = os.path.join(decrypted_files_dir, decrypted_files)

            #  Decrypting files using GnuPG
            os.system(
                'gpg --batch --pinentry-mode=loopback --yes --recipient ' + recipient + ' --encrypt -o ' + full_path_encrypted + ' ' + full_path_decrypted)

            #  Logging decrypted files
            print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* encrypting file {full_path_encrypted}')

    else:
        #  Logging decrypted files
        print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* Only variables string or list type are supported')
