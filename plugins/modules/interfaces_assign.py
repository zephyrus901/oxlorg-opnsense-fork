#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/interfaces.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.interfaces_assign import Assignment

except MODULE_EXCEPTIONS:
    module_dependency_error()

# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/interfaces_assign.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/interfaces_assign.html'


def run_module():
    module_args = {
        'if': dict(
            type='str', required=True, aliases=['device'],
            description="Raw device name (e.g. 'vtnet0', 'vlan0.10') to give an interface slot -- "
                        "the natural key this module matches existing assignments on. The "
                        "resulting assignment key ('wan'/'lan'/'optN') is always chosen by "
                        "OPNsense itself on create (sequential, next free optN) and can't be "
                        "requested here -- read it back from this module's own "
                        "diff.after.identifier (once created), or a subsequent search_item call",
        ),
        'descr': dict(type='str', required=False, default=''),
        'lock': dict(
            type='bool', required=False, default=False,
            description='Prevent this assignment from being removed until unlocked',
        ),
        **STATE_ONLY_MOD_ARG,
        **RELOAD_MOD_ARG,
        **OPN_MOD_ARGS,
    }

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

    module_wrapper(Assignment(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
