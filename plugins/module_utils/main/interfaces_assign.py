from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Assignment(BaseModule):
    # 'if' (the raw device, e.g. 'vlan0.10' or 'vtnet0') is the natural key -- OPNsense's own
    # AssignmentController always auto-assigns the real 'identifier' (wan/lan/optN) sequentially
    # on create and ignores whatever identifier a client submits (confirmed against
    # NetworkInterface::serializeToConfig(), core#9945/26.7). FIELD_PK reads the server-resolved
    # 'identifier' from the matched existing entry for all follow-up get/set/del calls -- never
    # from client input, since the server would ignore it anyway.
    FIELD_ID = 'if'
    FIELD_PK = 'identifier'
    CMDS = {
        'add': 'add_item',
        'del': 'del_item',
        'set': 'set_item',
        'search': 'search_item',
        'detail': 'get_item',
    }
    API_KEY_PATH = 'interface'
    API_MOD = 'interfaces'
    API_CONT = 'assignment'
    FIELDS_CHANGE = ['descr', 'lock']
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TYPING = {
        'bool': ['lock'],
        # get_item's detail response returns 'if' as a full select-field dict (every device
        # choice, whichever has 'selected': 1) unlike search_item's plain string -- confirmed
        # live 2026-07-20. get_selected() collapses either shape to the plain device string.
        'select': ['if'],
    }
    EXIST_ATTR = 'assignment'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.assignment = {}
