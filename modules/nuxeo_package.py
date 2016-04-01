#!/usr/bin/python
DOCUMENTATION = ''''''
EXAMPLES = ''''''

import json
import os
import subprocess

def main():
    module = AnsibleModule(
        argument_spec = dict(
            command=dict(required=False, default='nuxeoctl'),
            name=dict(required=True),
            path=dict(required=False),
            state=dict(default='present', choices=['present', 'absent'])
        )
    )

    command = module.params['command']
    target_package = module.params['name']
    desired_state = module.params['state']
    package_path = module.params['path']

    try:
        cmd_output = subprocess.check_output(['sudo', 'nuxeoctl', 'mp-list', '--json'])
    except subprocess.CalledProcessError as e:
        # Might fail if nuxeoctl is not found.
        module.fail_json(msg=e.output)

    # FIXME: 'nuxeoctl mp-list --json' RETURNS NON JSON OUTPUT WHEN THERE ARE TEMPLATES BEING IGNORED! JUUUULIAAAAAAAAN!!!!!!!
    try:
        json_output = json.loads(cmd_output)
    except:
        # If it fails we try to strip the non-json output by cutting everything before the first '{'.
        start_pos = cmd_output.find('{')
        cmd_output = cmd_output[start_pos:]
        #module.fail_json(msg=cmd_output)
        json_output = json.loads(cmd_output)

    packages = json_output['commands']['command']['packages']

    # TODO: Open issue with Nuxeo to return consistent JSON structure for all cases.
    package_installed = False
    # If no packages are installed 'packages' will be empty.
    if len(packages) > 0:
        # Actual packages are inside 'packages'
        package = packages['package']
        # If there is one package installed 'package' will be the actual package object.
        # If package is a dictionary we know its a package object.
        if type(package) is dict:
            # Handle single package case:
            if package['name'] == target_package:
                package_installed = True
        # If there are more than one package installed, 'package' will be a list.
        if type(package) is list:
            for p in package:
                if p['name'] == target_package:
                    package_installed = True
                    break

    # Absent -> Absent
    if package_installed == False and desired_state == 'absent':
        module.exit_json(changed=False, msg='already absent')

    # Present -> Present
    elif package_installed == True and desired_state == 'present':
        module.exit_json(changed=False, msg='already present')

    # Present -> Absent = uninstall.
    elif package_installed == True and desired_state == 'absent':
        try:
            cmd_output = subprocess.check_output(
                ['sudo', 'nuxeoctl', 'mp-remove', '--json', target_package] # Ignore output for now.
            )
            module.exit_json(changed=True, msg='uninstalled') # If the command didn't fail assume the package is gone.
        except subprocess.CalledProcessError as e:
            module.fail_json(msg=e.output) # Will fail if Nuxeo is running.

    # Absent -> present = install.
    elif package_installed == False and desired_state == 'present':
        #if package_path is None:
        #    module.fail_json(msg="Trying to install but no package path provided.")
        try:
            cmd_output = subprocess.check_output(
                ['sudo', 'nuxeoctl', 'mp-install', '--json', '--accept=true', target_package]
            ) # Ignore output for now.
            module.exit_json(changed=True, msg='installed') # If the command didn't fail assume the package is installed.
        except subprocess.CalledProcessError as e:
            module.fail_json(msg=e.output) # Will fail if Nuxeo is running.

    module.fail_json(msg="Unexpected logic path")

# import module snippets
from ansible.module_utils.basic import *

main()
