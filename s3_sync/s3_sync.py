#!/usr/bin/env python

"""

Read in setting values from ini file and then run s3 sync between local folder
and specified S3 bucket. Send results to local logfile & notify slack channel.

Use:
python s3_sync.py -i <settings_file.ini>

"""
try:
    import argparse
    import json
    import logging
    import os
    import requests
    import subprocess
    import sys
    from configparser import ConfigParser, ExtendedInterpolation
    from logbook import Logger, RotatingFileHandler
except ImportError as err:
    sys.exit(err)

# Instantiate argparse to get settings_file as argument
parser = argparse.ArgumentParser(description='.')
parser.add_argument('-i', dest="settings_file", required=True,
                    help='ini file containing configs', metavar='FILE')
args = parser.parse_args()
settings_file = args.settings_file

# Read settings_file
config = ConfigParser(interpolation = ExtendedInterpolation())
config.read(settings_file)

# Configure logbook logging
logger = RotatingFileHandler(config['Logs']['logfile'],
                             max_size = int(config['Logs']['max_size']),
                             backup_count = int(config['Logs']['backup_count']),
                             level = int(config['Logs']['level']))
logger.push_application()
logger = Logger(__name__)

# Get Computer name
computer_name = os.environ['COMPUTERNAME']


def verify_settings_file_exists(settings_file):
    """
    Verify that settings file exists.

    Args:
      settings_file (str): Path for the local settings file.

    Returns:
      If file exists, return None, otherwise exit.
    """
    if os.path.exists(settings_file):
        return
    else:
        logger.error("Settings file not found:", settings_file)
        sys.exit("[-] Settings file not found")


def set_environment_variables():
    """
    Set some of the read settings as environment variables.
    """
    os.environ['AWS_ACCESS_KEY_ID'] = config['AWS']['AWS_ACCESS_KEY_ID']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['AWS']['AWS_SECRET_ACCESS_KEY']
    os.environ['slack_webhook_url'] = config['Slack']['webhook_url']


def verify_local_folder_exists(local_video_records_done_folder):
    """
    Check whether the local video records done folder exists

    Args:
      local_video_records_done_folder (str): The path of the local video
        records done folder.

    Returns:
      If folder exists return None, and if not, logs error and exit.
    """
    if os.path.exists(local_video_records_done_folder):
        return
    else:
        logger.exception("Local Video Records Done folder not found")
        sys.exit("[-] Local Video Records Done folder not found")


def verify_aws_cli_installed(aws_cli_binary):
    """
    Check whether AWS CLI is installed

    Args:
      aws cli binary (str): absolute path to aws cli binary file.

    Returns:
      If file exists, return None, else log error and exit.

    """
    if os.path.exists(aws_cli_binary):
        return
    else:
        try:
            r = requests.get(config.get('AWS','CLI', fallback='https://s3.amazonaws.com/aws-cli/AWSCLI64.msi'), stream=True)
            with open('aws_cli.msi', 'wb') as fd:
                for chunk in r.iter_content(chunk_size=128):
                    fd.write(chunk)
            subprocess.run('msiexec /i aws_cli.msi /qn', check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except:
            logger.exception("Failed to install AWS CLI")
            sys.exit("[-] Failed to install AWS CLI")


def verify_s3_bucket_exists(s3_bucket_name):
    """
    Check whether S3 bucket exists

    Args:
      s3_bucket_name (str): The s3 bucket name

    Returns:
      list: if connection established and bucket found, return list of
        objects in bucket otherwise error and exit on any issues trying
        to list objects in bucket.
    """
    try:
        ls_s3_bucket_cmd = 'aws s3 ls {}'.format(s3_bucket_name)
        subprocess.run(ls_s3_bucket_cmd, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.SubprocessError:
        logger.exception("Failed to list specified s3 bucket")
        sys.exit("[-] Failed to list specified s3 bucket")


def notify_slack_channel(slack_message):
    """
    Send notification to Slack Channel

    Args:
      slack_message (str): message to send to slack
    """
    try:
        requests.post(os.environ.get('slack_webhook_url'),
                      json={"text": slack_message,
                            "username": config['Slack']['bot_username'],
                            "icon_emoji": config['Slack']['bot_emoji'], })
    except (requests.exceptions.RequestException, NameError) as err:
        logger.warn("Failed to notify slack channel with following error: {}", err)
        return


def sync_local_to_s3(local_video_records_done_folder, s3_bucket_name):
    """
    Sync local files to specified S3 bucket

    Args:
      local_video_records_done_folder (str): local folder containing video
        files ready to be copied to S3.
      s3_bucket_name (str): s3 bucket name
    """
    try:
        s3_sync_cmd = 'aws s3 sync {local_video_records_done_folder} "s3://"{s3_bucket_name}'.format(local_video_records_done_folder=local_video_records_done_folder, s3_bucket_name=s3_bucket_name)
        cmd_output = subprocess.run(s3_sync_cmd, check=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        logger.info("S3 sync successfully ran: {}", cmd_output)
        notify_slack_channel(f"Sync succeeded on: *{computer_name}* \n `str({cmd_output})`")
        logger.info("Syncing complete")
        return
    except subprocess.SubprocessError as err:
        logger.exception("Failed to sync local files to s3 bucket")
        notify_slack_channel(f"Sync failed: *{computer_name}* \n `{err}`")
        sys.exit("[-] Failed to sync local files to s3 bucket")


def main():
    set_environment_variables()
    verify_local_folder_exists(config['Paths']['local_video_records_done_folder'])
    verify_aws_cli_installed(config.get('Paths', 'aws_cli_binary', fallback='C:\Program Files\Amazon\AWSCLI\paws.exe'))
    verify_s3_bucket_exists(config['AWS']['s3_bucket_name'])
    sync_local_to_s3(config['Paths']['local_video_records_done_folder'], config['AWS']['s3_bucket_name'])


if __name__ == '__main__':
    main()
