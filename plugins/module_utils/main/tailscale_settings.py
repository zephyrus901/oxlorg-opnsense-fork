from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import GeneralModule


class Settings(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'settings'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'tailscale'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'loginTimeout', 'listenPort', 'acceptDNS', 'advertiseExitNode', 'useExitNode',
        'acceptSubnetRoutes', 'enableSSH', 'disableSNAT',
    ]
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TYPING = {
        'bool': [
            'enabled', 'acceptDNS', 'advertiseExitNode', 'acceptSubnetRoutes', 'enableSSH', 'disableSNAT',
        ],
        'int': ['loginTimeout', 'listenPort'],
    }
    INT_VALIDATIONS = {
        'listenPort': {'min': 1, 'max': 65535},
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
