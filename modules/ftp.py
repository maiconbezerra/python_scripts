import ftplib
import os
import socket
import time


def ftp_tls_connect(host, user, passwd):
    """
    Connect to FTP server using TLS

    :param host   - The FTP server hostname or IP address
    :param user   - The username to connect on server
    :param passwd - The password of user

    Returns the FTP connection state
    """

    print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* Trying to connect to host {host}')

    try:
        #  Connect to FTP Server
        ftps = ftplib.FTP_TLS(host=host, user=user, passwd=passwd)  # adds TLS support to FTP
        ftps.prot_p()  # Set up secure data connection

        print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* Connected to the FTP server {host}')
        return ftps

    except socket.gaierror:
        #  Treat connectivity or name resolution error
        print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* Fail to connect to host {host} (Connectivity error). '
                                                  f'Please check the connectivity or name resolution.')
        return 'ftp_connect_fail'

    except ftplib.error_perm:
        #  Treat permission error
        print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* Fail to connect to host {host} (User/Password invalid).'
                                                  f'Please check if you have a valid credential')
        return 'ftp_connect_fail'

    except Exception:
        #  Treat unknown error
        print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* Fail to connect to host {host} (Unexpected error).')

        return 'ftp_connect_fail'


def ftp_chg_dir(ftp_session, dir):
    """
    Changes the FTP directory context

    :param ftp_session - The FTP connection state (You can use ftp_tls_connect to get it)
    :param dir         - The name of the directory that you want to change

    Returns 'dir_found' if the directory exists and 'dir_not_found' if directory is not available
    """

    try:
        ftp_session.cwd('/')  # Inicia do diretorio root
        ftp_session.cwd(dir)
        print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* Directory changed to {dir}')
        return 'dir_found'

    except ftplib.error_perm:
        print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*ERROR* Directory {dir} not found')
        return 'dir_not_found'


def ls_ftp_files(ftp_session):
    """
    List files in FTP directory

    :param ftp_session - The FTP connection state (You can use ftp_tls_connect to get it)

    Returns a list of files in directory
    """

    ftp_list_files = list()

    ftp_session.retrlines('NLST', ftp_list_files.append)  # Pega arquivos do diretorio e coloca em uma lista temp

    for i in range(0, len(ftp_list_files)):  # Converte para lowercase
        ftp_list_files[i] = ftp_list_files[i].lower()

    print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* Listing files in directory')
    return ftp_list_files


def ftp_upload(files, upload_dir, ftp_session):
    """
    Upload files to FTP server

    :param files       - Files to upload to FTP server
    :param upload_dir  - Local path where the files are
    :param ftp_session - FTP Server connection state (Use ftp_tls_connect to retrieve)
    """

    for file in files:
        with open(os.path.join(upload_dir, file), "rb") as upload_file:
            ftp_session.storbinary(f"STOR {file}", upload_file)
        print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* Copying file {file} to ftp server')


def ftp_download(download_path, ftp_files, ftp_session):
    """
    Download files from FTP server

    :param download_path - Local path where the files will be stored
    :param ftp_files     - List of files in FTP server to download (Use ls_ftp_files to retrieve a list)
    :param ftp_session   - FTP Server connection state (Use ftp_tls_connect to retrieve)
    """

    print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* Starting download files to local path {download_path}')

    for i in ftp_files:
        local_path = os.path.join(download_path, i)

        with open(local_path, 'wb') as download_ftp_file:
            ftp_session.retrbinary('RETR ' + i, download_ftp_file.write)

        print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* Downloading {i}')

