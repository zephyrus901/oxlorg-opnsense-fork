#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/tailscale.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.tailscale_authentication import \
        Authentication

except MODULE_EXCEPTIONS:
    module_dependency_error()

# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/tailscale_authentication.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/tailscale_authentication.html'


def run_module():
    module_args = dict(
        loginServer=dict(
            type='str', required=False, default='https://controlplane.tailscale.com',
            aliases=['login_server'],
        ),
        preAuthKey=dict(
            type='str', required=False, default='', no_log=True, aliases=['pre_auth_key'],
            description='Plain, API-readable TextField (unlike DynDNS password) - a rotated key '
                        'IS detected as a real diff, masked only in the diff display',
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

    module_wrapper(Authentication(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
