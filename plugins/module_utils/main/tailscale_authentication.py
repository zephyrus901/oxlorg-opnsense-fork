from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import GeneralModule


class Authentication(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'authentication'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'tailscale'
    API_CONT = 'authentication'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = ['loginServer', 'preAuthKey']
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TYPING = {}
    FIELDS_DIFF_NO_LOG = ['preAuthKey']

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
