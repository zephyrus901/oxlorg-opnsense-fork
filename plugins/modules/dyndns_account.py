#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/dyndns.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.dyndns_account import Account

except MODULE_EXCEPTIONS:
    module_dependency_error()

# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/dyndns_account.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/dyndns_account.html'


def run_module():
    module_args = dict(
        description=dict(
            type='str', required=True,
            description='Unique per-account identity - the natural key this module matches '
                        'existing accounts on (1-255 characters)',
        ),
        service=dict(
            type='str', required=False, default='', choices=[
                '', 'hosting1984', 'changeip', 'cloudflare', 'cloudns', 'digitalocean', 'dinahosting',
                'dnsmadeeasy', 'dns-o-matic', 'dnsexit2', 'dyndns2', 'dnspark', 'dnspodcn', 'dslreports1',
                'dondominio', 'duckdns', 'dynu', 'easydns', 'freedns', 'freemyip', 'gandi', 'godaddy',
                'googledomains', 'he-net', 'he-net-tunnel', 'hetzner', 'inwx', 'keysystems', 'loopia',
                'mythicdyn', 'namecheap', 'nfsn', 'njalla', 'noip', 'nsupdatev4', 'nsupdatev6', 'ovh',
                'porkbun', 'regfishde', 'servercow', 'sitelutions', 'spdyn', 'strato', 'woima', 'yandex',
                'zoneedit1', 'custom',
            ],
            description='Dynamic DNS provider',
        ),
        protocol=dict(
            type='str', required=False, default='', choices=['', 'dyndns1', 'dyndns2', 'get', 'post', 'put'],
            description="Only relevant when 'service' is 'custom'",
        ),
        server=dict(type='str', required=False, default=''),
        username=dict(
            type='str', required=False, default='',
            description="For Cloudflare API-token auth, ddclient's own convention is the literal "
                        "value 'token' (selects token auth over the global-key auth path)",
        ),
        password=dict(
            type='str', required=False, default='', no_log=True,
            description='UpdateOnlyTextField on the OPNsense side - never returned by the API, so '
                        'this module cannot diff a rotated value against the current one; a token '
                        'rotation alone (no other field changed) needs no_log-safe re-application by '
                        'the caller',
        ),
        resourceId=dict(type='str', required=False, default='', aliases=['resource_id']),
        hostnames=dict(
            type='list', elements='str', required=True,
            description='Comma-separated on the wire (HostnameField, AsList) - hostnames to keep updated',
        ),
        wildcard=dict(type='bool', required=False, default=False),
        zone=dict(type='str', required=False, default=''),
        checkip=dict(
            type='str', required=False, default='',
            description="How the current IP is determined - 'if' reads the given 'interface' "
                        "directly (no external dependency); other values select one of the plugin's "
                        "web-checker providers. Not locally enum-validated - the OPNsense OptionField "
                        "remaps some of these key names via a 'value' XML attribute the module doesn't "
                        "re-derive, so an invalid choice fails loud from the live API instead of a "
                        "possibly-wrong local guess.",
        ),
        dynipv6host=dict(type='str', required=False, default=''),
        checkip_timeout=dict(type='int', required=False, default=10),
        force_ssl=dict(type='bool', required=False, default=True),
        ttl=dict(type='int', required=False, default=300),
        interface=dict(
            type='str', required=False, default='',
            description="Required when 'checkip' is 'if'",
        ),
        **STATE_MOD_ARG,
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

    module_wrapper(Account(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
