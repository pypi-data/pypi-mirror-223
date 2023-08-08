import json
import logging
import os
import subprocess
from rc.cli.utils import RctlValidSubprocessError, get_repo
import tempfile
from rc.utils.request import RctlValidRequestError, get_config_value_by_key, update_repo_lock
from rc.utils import DEBUG
from datetime import datetime

LOG_FILE = "rc.log"

logger = logging.getLogger(__name__)
level = logging.INFO

def log_setup(args = None):
    if DEBUG:
        level = logging.DEBUG
        logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')     
    elif args:
        if args.output:
            level = logging.DEBUG
            logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S') 
    else:
        # Get the temporary directory path
        temp_dir = tempfile.gettempdir()
        logger.setLevel(logging.DEBUG)
        # Create a file handler and set the logging level
        log_file_path = os.path.join(temp_dir, LOG_FILE)
        file_handler = logging.FileHandler(log_file_path, mode='w')
        file_handler.setLevel(logging.DEBUG)
        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Add the formatter to the file handler
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)


log_setup()

def upload_log():
    CLOUD_STORAGE = get_config_value_by_key('cloud_storage')
    temp_dir = tempfile.gettempdir()
    log_file_path = os.path.join(temp_dir, LOG_FILE)

    CLOUD_STORAGE_BUCKET = get_config_value_by_key('bucket_name')
    CLOUD_STORAGE_DIR = get_config_value_by_key('cloud_storage_dir')
    SECRET = get_config_value_by_key('minio_secret_key') if CLOUD_STORAGE == 'minio' else get_config_value_by_key('s3_storage_secret_key')
    ACCESS = get_config_value_by_key('minio_access_key') if CLOUD_STORAGE == 'minio' else get_config_value_by_key('s3_storage_access_key')
    MINIO_URL = get_config_value_by_key('minio_url')
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"rc_{current_datetime}.log"
    repo = get_repo()
    if repo:
        dest = f"{CLOUD_STORAGE_DIR}/{repo}/logs/{log_filename}"
    else:
        dest = f"{CLOUD_STORAGE_DIR}/logs/{log_filename}"
    import botocore.session   
    # Create a botocore session with the AWS access key and secret key
    session = botocore.session.Session()
    session.set_credentials(ACCESS, SECRET)

    if CLOUD_STORAGE == 'minio':
        s3 = session.create_client('s3', endpoint_url=MINIO_URL)
    else:
        s3 = session.create_client('s3')

    # Upload the file to S3
    with open(log_file_path, 'rb') as file:
        s3.put_object(Bucket=CLOUD_STORAGE_BUCKET, Key=dest, Body=file)         
class RctlParserError(Exception):
    """Base class for CLI parser errors."""
    def __init__(self):
        logger.error("Parser error")
        super().__init__("Parser error")

class RctlValidReqError(Exception):
    def __init__(self, msg, *args):
        assert msg
        self.msg = msg
        logger.error(msg)
        super().__init__(msg, *args)

def parse_args(argv=None):
    from .parser import get_main_parser
    try:
        parser = get_main_parser()
        args = parser.parse_args(argv)
        args.parser = parser
        return args
    except RctlParserError as exc:
        pass

def valid_requirement():
    try:        
        subprocess.run(['gh', '--version'], capture_output=True)
    except OSError as err:        
        raise RctlValidRequestError('ERROR: git hub cli not found! Please install git hub cli from https://cli.github.com')
    try:        
        subprocess.run(['git', '--version'], capture_output=True)
    except OSError as err:        
        raise RctlValidRequestError('git not found! Please install git')
        

def main(argv=None):
    try:
        os.environ['GH_TOKEN'] = get_config_value_by_key('gh_token')
        valid_requirement()
        args = parse_args(argv)
        cmd = args.func(args)
        cmd.do_run()
        upload_log()
    except KeyboardInterrupt as exc:
        logger.debug(exc)
        upload_log()
    except RctlValidRequestError as exc:
        logger.debug(exc)
        upload_log()
    except RctlValidSubprocessError as exc:
        print(exc.msg)
    except Exception as exc:
       logger.exception(exc)
       logger.debug(exc)
       upload_log()
    
