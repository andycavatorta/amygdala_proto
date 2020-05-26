"""
This file contains the default config data for the reports system

On start-up thirtybirds loads config data.  It loads default configs from config/ unless otherwise specified.  New config data can be loaded dynamically at runtime.

Typical usage example:

from config import reports

foo = ClassFoo(reports.foo_config)

"""

class Roles():
    controller_hostname="FERAL"
    hosts={
        "FERAL":"controller",
        "amygdala":"sliders"
    }

class Reporting():
    app_name = "amygdala"
    #level = "ERROR" #[DEBUG | INFO | WARNING | ERROR | CRITICAL]
    #log_to_file = True
    #print_to_stdout = True
    publish_to_dash = True
    
    class Status_Types:
        EXCEPTIONS = True
        INITIALIZATIONS = True
        NETWORK_CONNECTIONS = True
        NETWORK_MESSAGES = True
        SYSTEM_STATUS = True
        VERSION_STATUS = True
        ADAPTER_STATUS = True

class Version_Control():
    update_on_start = False
    github_repo_owner = "andycavatorta"
    github_repo_name = "amygdala"
    branch = "master"

class Roboteq:
    "boards":{
        "300:1058:3014688:1429493507:540422710":{},
        "300:1058:2031663:1429493506:540422710":{},
    },
    "motors":{
        "pitch_slider":{
            "mcu_id":"300:1058:2031663:1429493506:540422710",
            "channel":"1",
        },
        "bow_position_slider":{
            "mcu_id":"300:1058:2031663:1429493506:540422710",
            "channel":"2",
        },
        "bow_height":{
            "mcu_id":"300:1058: 3014688:1429493507:540422710",
            "channel":"1",
        },
        "bow_rotation":{
            "mcu_id":"300:1058:3014688:1429493507:540422710",
            "channel":"2",
        }
    }

