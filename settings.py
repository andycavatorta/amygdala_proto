"""
This file contains the default config data for the reports system

On start-up thirtybirds loads config data.  It loads default configs from config/ unless otherwise specified.  New config data can be loaded dynamically at runtime.

Typical usage example:

from config import reports

foo = ClassFoo(reports.foo_config)

"""

class Network():
    controller_hostname="FERAL"
    discovery_multicast_group = "224.3.29.71"
    discovery_multicast_port = 10020
    discovery_response_port = 10021
    pubsub_pub_port = 10022
    pubsub_pub_port2 = 10024

class Reporting():
    app_name = "amygdala"
    level = "ERROR" #[DEBUG | INFO | WARNING | ERROR | CRITICAL]
    print_to_stdout = True
    log_to_file = True
    publish_to_dash = True

class Version_Control():
    github_repo_owner = "andycavatorta"
    github_repo_name = "amygdala"
    branch = "master"




