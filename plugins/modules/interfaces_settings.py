#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/interfaces.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.interfaces_settings import Settings

except MODULE_EXCEPTIONS:
    module_dependency_error()

# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/interfaces_settings.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/interfaces_settings.html'


def run_module():
    module_args = dict(
        disablechecksumoffloading=dict(
            type='bool', required=False, default=False, aliases=['disable_checksum_offloading'],
        ),
        disablesegmentationoffloading=dict(
            type='bool', required=False, default=False, aliases=['disable_segmentation_offloading'],
        ),
        disablelargereceiveoffloading=dict(
            type='bool', required=False, default=False, aliases=['disable_large_receive_offloading'],
        ),
        disablevlanhwfilter=dict(
            type='bool', required=False, default=False, aliases=['disable_vlan_hw_filter'],
            description="Disabling this is what actually drops VLAN_HWTAGGING/VLAN_HWTSO from "
                        "ifconfig (confirmed live) -- a global toggle, only takes effect per-device "
                        "when that device's own 'hw_settings_overwrite' flag is unset (no API model "
                        "covers that flag; clear it via config.xml/SSH-PHP if this no-ops)",
        ),
        **RELOAD_MOD_ARG,
        **OPN_MOD_ARGS,
    )

    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        }
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    module_wrapper(Settings(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
