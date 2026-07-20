from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import GeneralModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import is_true

# GET's response shape for this one field, confirmed live 2026-07-20 -- unlike the other 3
# plain-bool fields, it's a genuine 3-way select (fixed positional order, no keys):
#   [{"value": "Enable VLAN Hardware Filtering", "selected": 0},
#    {"value": "Disable VLAN Hardware Filtering", "selected": 1},
#    {"value": "Leave default", "selected": 0}]
# index 1 ("Disable") is the only state this role ever sets -- POST still accepts a plain "1"/"0"
# for it (confirmed live: POST {"disablevlanhwfilter": 1} -> {"result": "saved"}), only the GET
# side needs this custom extraction.
DISABLED_INDEX = 1


class Settings(GeneralModule):
    # Global toggle -- applied per-device by FreeBSD's own _interfaces_hardware() only when
    # that device's own 'hw_settings_overwrite' flag is unset (no MVC/API model covers that
    # flag; a device with it already set silently ignores this global toggle regardless).
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'settings'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'interfaces'
    API_CONT = 'settings'
    FIELDS_CHANGE = [
        'disablechecksumoffloading', 'disablesegmentationoffloading',
        'disablelargereceiveoffloading', 'disablevlanhwfilter',
    ]
    FIELDS_ALL = list(FIELDS_CHANGE)
    FIELDS_TYPING = {
        # covers the SEND side (bool -> "1"/"0") for all 4 fields, including disablevlanhwfilter
        # -- the base bool conversion can't parse its list-shaped GET response, so
        # simplify_existing() below re-derives that one field's value after the base call.
        'bool': FIELDS_CHANGE,
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)

    def simplify_existing(self, existing: dict) -> dict:
        raw_filter = existing.get('disablevlanhwfilter')
        simplified = GeneralModule.simplify_existing(self, existing)

        if isinstance(raw_filter, list):
            simplified['disablevlanhwfilter'] = any(
                idx == DISABLED_INDEX and is_true(opt.get('selected'))
                for idx, opt in enumerate(raw_filter)
            )

        return simplified
