import argparse
import json
import logging
import os
from datetime import timedelta
import sys 
from timeit import default_timer as timer
import os, pwd

from rc.cli.command import CmdBase
from rc.cli.utils import current_commit_hash, folder_exists, is_repo_exist_in_gh, run_command_on_subprocess, repo_name_valid, get_git_url, upload_model_file_list_json
from rc.utils import RC_BASE_URL
from rc.utils.config import create_rc_folder, set_config_value
from rc.utils.request import RctlValidRequestError, get_config_value_by_key, create_repository, create_repo_lock, get_repository, insert_repo_commit
from rc.cli import log_setup
from rc.cli.utils import RctlValidSubprocessError, get_repo

logger = logging.getLogger(__name__)
   
 

"""
----------------------------
***Bucket Name Validation***
----------------------------
Bucket names should not contain upper-case letters
Bucket names should not contain underscores (_)
Bucket names should not end with a dash
Bucket names should be between 3 and 63 characters long
Bucket names cannot contain dashes next to periods (e.g., my-.bucket.com and my.-bucket are invalid)
Bucket names cannot contain periods - Due to our S3 client utilizing SSL/HTTPS, Amazon documentation indicates that a bucket name cannot contain a period, otherwise you will not be able to upload files from our S3 browser in the dashboard.
"""

class RepoMain():
    def __init__(self) -> None:
        self.CLOUD_STORAGE = get_config_value_by_key('cloud_storage')
        self.CLOUD_STORAGE_BUCKET = get_config_value_by_key('bucket_name')
        self.CLOUD_STORAGE_DIR = get_config_value_by_key('cloud_storage_dir')
        self.CLOUD_STORAGE_LOCATION = f"s3://{self.CLOUD_STORAGE_BUCKET}/{self.CLOUD_STORAGE_DIR}"
        self.MINIO_URL = get_config_value_by_key('minio_url') if self.CLOUD_STORAGE == 'minio' else ""
        self.INITIAL_COMMIT = get_config_value_by_key('git_initial_commit')
        self.GIT_BRANCH = get_config_value_by_key('git_initial_branch')
        self.GIT_ORG = get_config_value_by_key('git_org')
        self.AUTH_TOKEN = get_config_value_by_key('auth_token')
        self.TAGS = {"dataset", "model"}
        self.created_by = pwd.getpwuid(os.getuid()).pw_name 
        self.RC_WEB_BACKEND_URL = get_config_value_by_key('web_backend_url')
        self.RC_INFLUX_BACKEND_URL = get_config_value_by_key('influx_backend_url')
        
    def run_git_commands(self,repo_name, repo_tag, target_dir):
        repo_dir = repo_name if not target_dir else target_dir 
        run_command_on_subprocess("git add .rc", repo_dir)       
        run_command_on_subprocess("git commit -m '{0}' -a".format(self.INITIAL_COMMIT), repo_dir)    
        run_command_on_subprocess("git branch -M {0}".format(self.GIT_BRANCH), repo_dir)    
        run_command_on_subprocess("git push --set-upstream origin {0}".format(self.GIT_BRANCH), repo_dir)

    def run_repo_create_subprocesses(self,repo_name, repo_tag, target_dir):    
        repo_dir = repo_name if not target_dir else target_dir 
        logger.debug(f"Repository Name: {repo_name}")
        secret_key = get_config_value_by_key('minio_secret_key') if self.CLOUD_STORAGE == 'minio' else get_config_value_by_key('s3_storage_secret_key')
        access_key = get_config_value_by_key('minio_access_key') if self.CLOUD_STORAGE == 'minio' else get_config_value_by_key('s3_storage_access_key')
        if repo_tag =="dataset":
            run_command_on_subprocess("gh config set git_protocol ssh")  
            if not target_dir:
                run_command_on_subprocess("gh repo create {0}/{1} --private --clone".format(self.GIT_ORG, repo_name))    
            run_command_on_subprocess("dvc init", repo_dir)    
            run_command_on_subprocess("dvc remote add -d {0} {1}/{2} -f".format(self.CLOUD_STORAGE_BUCKET, self.CLOUD_STORAGE_LOCATION, repo_name), repo_dir)   
            if self.CLOUD_STORAGE == 'minio':        
                run_command_on_subprocess("dvc remote modify {0} endpointurl {1}".format(self.CLOUD_STORAGE_BUCKET, self.MINIO_URL, repo_name), repo_dir)           
            run_command_on_subprocess("dvc remote modify {0} secret_access_key {1}".format(self.CLOUD_STORAGE_BUCKET,secret_key ), repo_dir)         
            run_command_on_subprocess("dvc remote modify {0} access_key_id {1}".format(self.CLOUD_STORAGE_BUCKET, access_key), repo_dir)        
            run_command_on_subprocess("dvc config core.autostage true", repo_dir)            
        if repo_tag == "model":
            run_command_on_subprocess("gh config set git_protocol ssh") 
            if not target_dir: 
                run_command_on_subprocess("gh repo create {0}/{1} --private --clone".format(self.GIT_ORG, repo_name)) 
            run_command_on_subprocess("touch README.md", repo_dir)      
            run_command_on_subprocess("git add README.md", repo_dir)       

        configs = {
            "repo":repo_name,
            "git_org":self.GIT_ORG,
            "remote_bucket":self.CLOUD_STORAGE_BUCKET,
            "remote_bucket_dir":self.CLOUD_STORAGE_DIR,
            "remote_bucket_location":self.CLOUD_STORAGE_LOCATION,
            "minio_url":get_config_value_by_key('minio_url'),
            "secret_key":secret_key,
            "access_key":access_key,
            "version":0,
            "repo_id":"", 
            "tag":repo_tag,
            "auth_token":self.AUTH_TOKEN,
            "base_url": RC_BASE_URL,
            "web_backend_url": self.RC_WEB_BACKEND_URL,
            "influx_backend_url": self.RC_INFLUX_BACKEND_URL,
            "org_id":18,
            "project_id":2
        }  
        create_rc_folder(repo_name, configs, target_dir)

    
    def create_repo(self, args):
        print("Repo creating...")  
        if self.check_git_init() and not args.target:
            print("The repo creating process inside the repository is not possible.")
            sys.exit(50)
        logger.debug(f"START CREATE REPO COMMAND")
        repository_name = args.name    
        repository_tag = args.tag 
        target_dir = args.target 
        repo_dir = repository_name if not target_dir else target_dir 
        if is_repo_exist_in_gh("{0}/{1}".format(self.GIT_ORG, repository_name)) and not args.target:
            print("The repo creating process could not be completed because the repo already exists. Please rename repo and try again.")
            sys.exit(50)

        if folder_exists(repository_name):
            print("The repo creating process could not be completed because the directory already exists. Please rename repo and try again.")
            sys.exit(50)

        if repository_tag not in self.TAGS:
            logger.error("'{0}' tag is not available. Please select from {1}".format(repository_tag, self.TAGS))
            sys.exit(50)   
        self.run_repo_create_subprocesses(repository_name, repository_tag, target_dir)
        git_repo = get_git_url(repo_dir)
        
        if repository_tag == "dataset":

            s3_repo = "{1}/{2}".format(self.CLOUD_STORAGE_BUCKET, self.CLOUD_STORAGE_LOCATION, repository_name)  

            req_body = json.dumps({
                "repo_name":repository_name,
                "tag":repository_tag,
                "created_by":self.created_by,
                "git_repo":git_repo.replace('\n', ''),
                "remote_storage_url":s3_repo,
            })

            logger.debug(req_body)

        if repository_tag == "model":
            req_body = json.dumps({
                "repo_name":repository_name,
                "tag":repository_tag,
                "created_by":self.created_by,
                "git_repo":git_repo.replace('\n', ''),
            })
            logger.debug(req_body)

        created_repo_data = create_repository(req_body)
        set_config_value("repo_id", created_repo_data['id'], repo_dir)
        
        if repository_tag == "dataset":
            self.run_git_commands(repository_name, repository_tag, target_dir)

        if repository_tag == "model":
            set_config_value("version", 1, repo_dir)
            self.run_git_commands(repository_name, repository_tag, target_dir)
            commit_hash = current_commit_hash(repo_dir)
            request_payload = {
                    "commit_message" : "Initial commit",
                    "repo" : repository_name,
                    "commit_id":commit_hash,
                    "version":0,
                    "branch":"master"
                }  
            insert_repo_commit(json.dumps(request_payload))
            upload_model_file_list_json(commit_hash, repo_dir)

        create_repo_lock(json.dumps({"repo_name":repository_name, "user_name":self.created_by, "locked":False}))
        print("Repository has been created. `cd {}`".format(repository_name))  

        logger.debug(f"END CREATE REPO COMMAND")
    
    def check_git_init(self):
        current_dir = os.getcwd()
        while current_dir != '/':  # Stop when we reach the root directory
            if os.path.exists(os.path.join(current_dir, '.git')):
                return True  # .git folder exists, so project has been initialized
            current_dir = os.path.dirname(current_dir)
        return False

    def clone_repo(self, args):
        if self.check_git_init():
            print("The repo cloning process inside the repository is not possible.")
            sys.exit(50)
        start = timer()
        repository_name = args.name  

        if folder_exists(repository_name):
            print("The repo cloning process could not be completed because the directory already exists.")
            sys.exit(50)

        print('Cloning...')
        run_command_on_subprocess("git clone git@github.com:{0}/{1}.git".format(self.GIT_ORG, repository_name), None, True)    
        tag = get_repository(repository_name)
        if tag == "dataset":
            run_command_on_subprocess("dvc pull", repository_name, True) 
        print("Repository cloned successfully")
        end = timer()
        logger.debug('CLONE TIME {0}'.format(timedelta(seconds=end-start)))    


class CmdRepo(CmdBase):
    def __init__(self, args):
        log_setup(self.args) 
        super().__init__(args)   
        self.repo = RepoMain()     
        if getattr(self.args, "name", None):
            self.args.name = self.args.name.lower()            
            repo_name_valid(self.args.name)
        else:
            target_value = getattr(self.args, "target", None)
            if target_value is not None and target_value != ".":
                print("Invalid target value. The target should be a dot (.). Root dir location of repo.")
                sys.exit(1)
            if target_value:
                self.args.name = get_repo(target_value).lower()
                if self.args.create:
                    if not self.repo.check_git_init() and target_value:
                        print("The repo creating process could not be completed because the target dir does not contain git")
                        sys.exit(50)
                repo_name_valid(self.args.name)
            elif target_value is None:
                raise RctlValidRequestError("Error: Please provide a valid name, -n")
class CmdRepoCreate(CmdRepo):
    def run(self):          
        if self.args.create:
            self.repo.create_repo(self.args)
        if self.args.clone:
            self.repo.clone_repo(self.args)                                    
        return 0


def add_parser(subparsers, parent_parser):
    REPO_HELP = "Create a new repository."
    REPO_DESCRIPTION = (
        "Create a new repository."
    )

    repo_parser = subparsers.add_parser(
        "repo",
        parents=[parent_parser],
        description=REPO_DESCRIPTION,
        help=REPO_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    repo_parser.add_argument(
        "-create",
        "--create",
        action="store_true",
        default=False,
        help="Create new repo",
    )

    repo_parser.add_argument(
        "-clone",
        "--clone",
        action="store_true",
        default=False,
        help="Clone new repo",
    )

    repo_parser.add_argument(
        "-n", 
        "--name", 
        nargs="?", 
        help="Name of the repo",
    )


    repo_parser.add_argument(
        "-tag", 
        "--tag", 
        nargs="?", 
        help="Tag of the repo",
    )

    repo_parser.add_argument(
        "-t", 
        "--target", 
        nargs="?", 
        help="Target of the repo",
    )

    repo_parser.add_argument(
        "-o", 
        "--output", 
        type=bool, 
        nargs='?',
        const=True, 
        default=False,
        help="Output debug",
    )
    
    repo_parser.set_defaults(func=CmdRepoCreate)
