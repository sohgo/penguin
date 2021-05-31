from pydantic import BaseModel, Extra
from pydantic import validator
from typing import List, Optional, Union, Any
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from os import environ
from setlogger import set_logger
import logging
import json

class Config(BaseModel):
    db_name: str = "patients"
    table_name: str = "entry"
    mongodb_url: str = "mongodb://127.0.0.1:27017/apitest?retryWrites=true&w=majority"
    log_file: str
    log_stdout: bool = False
    enable_debug: bool = False
    tz: str = "Asia/Tokyo"
    server_address: str
    server_port: int = 8082
    server_cert: Union[str, None]
    enable_tls: bool = False
    logger: Any
    loop: Any

    @validator("enable_tls", always=True)
    def update_enable_tls(cls, v, values, config, **kwargs):
        return True if values["server_cert"] else False

    class Config():
        extra = Extra.forbid

def __from_args(args):
    ap = ArgumentParser(
            description="PEN Backend server.",
            formatter_class=ArgumentDefaultsHelpFormatter)
    ap.add_argument("config_file", metavar="CONFIG_FILE",
                    help="specify the config file.")
    ap.add_argument("-d", action="store_true", dest="enable_debug",
                help="enable debug mode.")
    ap.add_argument("-D", action="store_true", dest="log_stdout",
                help="enable to show messages onto stdout.")
    opt = ap.parse_args(args)
    environ["PEN_CONFIG_FILE"] = opt.config_file
    environ["PEN_ENABLE_DEBUG"] = str(opt.enable_debug)
    environ["PEN_LOG_STDOUT"] = str(opt.log_stdout)

def set_config(loop, args=None):
    def get_env_bool(optval, envkey):
        c = environ.get(envkey)
        if c is None:
            return optval
        elif c.upper() in [ "TRUE", "1" ]:
            return True
        elif c.upper() in [ "FALSE", "0" ]:
            return False
        else:
            raise ValueError(f"ERROR: {key} must be bool, but {c}")

    """
    priority order
        1. cli arguments.
        2. environment variable.
        3. config file.
    """
    if args is not None:
        __from_args(args)
    # load the config file.
    config_file = environ["PEN_CONFIG_FILE"]
    try:
        config = Config.parse_obj(json.load(open(config_file)))
    except Exception as e:
        print("ERROR: {} read error. {}".format(config_file, e))
        exit(1)
    # overwrite the config by the cli options/env variable.
    get_env_bool(config.enable_debug, "PEN_ENABLE_DEBUG")
    get_env_bool(config.log_stdout, "PEN_LOG_STDOUT")
    # update config.
    config.loop = loop
    config.logger = set_logger(logging,
                               prog_name="pendb",
                               log_file=config.log_file,
                               logging_stdout=config.log_stdout,
                               debug_mode=config.enable_debug)
    return config

if __name__ == "__main__":
    import sys
    conf = json.load(open(sys.argv[1]))
    m = Config.parse_obj(conf)
    print(m)
