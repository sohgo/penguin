#!/usr/bin/env python

import sys
from feconf import set_config
import uvicorn
from feapi import api

def log_start(config, logger):
    logger.info("Starting PEN Frontend server listening on {}://{}:{}/"
                .format("https" if config.server_cert else "http",
                        config.server_address if config.server_address else "*",
                        config.server_port))

if __name__ == "__main__":
    import uvicorn
    config, logger = set_config(sys.argv[1:])
    log_start(config, logger)
    uvicorn.run(api(config, logger),
                host=config.server_address,
                port=config.server_port,
                ssl_certfile=config.server_cert if config.server_cert else None,
                debug=config.enable_debug)
else:
    config, logger = set_config()
    log_start(config, logger)
    app = api(config, logger)

