"""
This file contains all the cloud related utils.
"""
import glob
import os

import paramiko


def get_files_and_upload():
    """
    Look for files in the current main directory and upload to sftp
    :return:
    """
    path = "/tmp/*.csv"
    # Get the credentials from the environment
    SFTP_USER_NAME = os.environ.get('SFTP_USER_NAME')
    SFTP_PASSWORD = os.environ.get('SFTP_PASSWORD')
    SFTP_LOCATION = os.environ.get('SFTP_LOCATION', '')
    SFTP_HOST = os.environ.get('SFTP_HOST')
    SFTP_PORT = 22
    for fname in glob.glob(path):
        with open(fname) as csv_file:
            print(csv_file.name)
            transport = paramiko.Transport(
                (SFTP_HOST, SFTP_PORT),
                default_window_size=paramiko.common.MAX_WINDOW_SIZE
            )
            transport.connect(username=SFTP_USER_NAME, password=SFTP_PASSWORD)
            connection = paramiko.SFTPClient.from_transport(transport)
            if SFTP_LOCATION:
                connection.chdir(SFTP_LOCATION)
            connection.put(csv_file.name, csv_file.name.split("/")[-1])
