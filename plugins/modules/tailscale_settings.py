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
        EN_ONLY_MOD_ARG, OPN_MOD_ARGS, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.tailscale_settings import Settings

except MODULE_EXCEPTIONS:
    module_dependency_error()

# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/tailscale_settings.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/tailscale_settings.html'


def run_module():
    module_args = dict(
        loginTimeout=dict(type='int', required=False, default=10, aliases=['login_timeout']),
        listenPort=dict(type='int', required=False, default=41641, aliases=['listen_port']),
        acceptDNS=dict(type='bool', required=False, default=True, aliases=['accept_dns']),
        advertiseExitNode=dict(
            type='bool', required=False, default=False, aliases=['advertise_exit_node'],
        ),
        useExitNode=dict(
            type='str', required=False, default='', aliases=['use_exit_node'],
            description="Selects an existing peer (by its Tailscale node key) to route this "
                        "firewall's own egress through. Its option list is populated live via "
                        "'tailscale tailscale-status', not a static enum - leave unset when this "
                        "node only advertises an exit node rather than consuming one.",
        ),
        acceptSubnetRoutes=dict(
            type='bool', required=False, default=False, aliases=['accept_subnet_routes'],
        ),
        enableSSH=dict(type='bool', required=False, default=False, aliases=['enable_ssh']),
        disableSNAT=dict(type='bool', required=False, default=False, aliases=['disable_snat']),
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

    module_wrapper(Settings(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
