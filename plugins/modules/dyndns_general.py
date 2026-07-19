#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/dyndns.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        EN_ONLY_MOD_ARG, OPN_MOD_ARGS, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.dyndns_general import General

except MODULE_EXCEPTIONS:
    module_dependency_error()

# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/dyndns_general.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/dyndns_general.html'


def run_module():
    module_args = dict(
        backend=dict(
            type='str', required=False, default='opnsense', choices=['ddclient', 'opnsense'],
            description="Dynamic DNS update backend - 'opnsense' is the native PHP-based backend "
                        "(the plugin's own default), 'ddclient' uses the classic ddclient daemon"
        ),
        verbose=dict(
            type='bool', required=False, default=False,
            description='Log verbosely to help with troubleshooting',
        ),
        allowipv6=dict(
            type='bool', required=False, default=False, aliases=['allow_ipv6'],
            description='Allow the use of IPv6 to perform update requests',
        ),
        **EN_ONLY_MOD_ARG,
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

    module_wrapper(General(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
