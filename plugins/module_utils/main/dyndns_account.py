from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Account(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'add_item',
        'del': 'del_item',
        'set': 'set_item',
        'search': 'search_item',
        'detail': 'get_item',
        'toggle': 'toggle_item',
    }
    API_KEY_PATH = 'account'
    API_MOD = 'dyndns'
    API_CONT = 'accounts'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'enabled', 'service', 'protocol', 'server', 'username', 'password', 'resourceId',
        'hostnames', 'wildcard', 'zone', 'checkip', 'interface', 'dynipv6host',
        'checkip_timeout', 'force_ssl', 'ttl',
    ]
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_OPTIONAL = ['password']
    FIELDS_DIFF_NO_LOG = ['password']
    FIELDS_TYPING = {
        'bool': ['enabled', 'wildcard', 'force_ssl'],
        'select': ['service', 'protocol', 'checkip'],
        'list': ['hostnames', 'interface'],
        'int': ['checkip_timeout', 'ttl'],
    }
    STR_LEN_VALIDATIONS = {
        'description': {'min': 1, 'max': 255},
    }
    INT_VALIDATIONS = {
        'checkip_timeout': {'min': 10, 'max': 60},
        'ttl': {'min': 1, 'max': 604800},
    }
    EXIST_ATTR = 'account'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.account = {}

    def check(self) -> None:
        if self.p['state'] == 'present' and self.p['checkip'] == 'if' and is_unset(self.p['interface']):
            self.m.fail_json(
                "You need to provide an 'interface' when 'checkip' is set to 'if'!"
            )

        self._base_check()
