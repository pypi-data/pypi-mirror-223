

import argparse
import logging
from rc.cli.command import CmdBase
from rc.cli import log_setup
from rc.utils.raga_config_reader import read_raga_config, get_config_value


logger = logging.getLogger(__name__)

class CmdList(CmdBase):
    def __init__(self, args):
        super().__init__(args)
    
    def run(self):
        log_setup(self.args)
        config_data = read_raga_config()
        raga_secret_access_key = get_config_value(config_data, 'default', 'rc_base_url')
        print(raga_secret_access_key)
            
            

def add_parser(subparsers, parent_parser):
    REPO_HELP = "Check codes for Developer"
    REPO_DESCRIPTION = (
        "Check codes for Developer"
    )

    repo_parser = subparsers.add_parser(
        "check",
        parents=[parent_parser],
        description=REPO_DESCRIPTION,
        help=REPO_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
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
    repo_parser.set_defaults(func=CmdList)