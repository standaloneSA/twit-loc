#!/usr/bin/env python

import os
import sys
import json
import configparser

cfg_file = 'config'
def get_secrets():
    # These are the secrets that we care about
    secret_list = {
        "api_key": "",
        "api_secret_key": "",
        "access_token": "",
        "access_token_secret": ""
        }

    # Check the config file for secrets
    parser = configparser.ConfigParser()
    cfg = parser.read(cfg_file)
    if len(cfg) != 1:
        print("Error reading file '%s'" % cfg_file)
        sys.exit(1)
    secrets = parser._sections['secrets']

    for secret in secret_list:
        secret_list[secret] = secrets.get(secret)

    # Environmental variables override config files
    for secret in secret_list:
        if os.environ.get(secret):
            secret_list[secret] = os.environ.get(secret)

    return secret_list

if __name__ == '__main__':
    print(json.dumps(get_secrets()))
