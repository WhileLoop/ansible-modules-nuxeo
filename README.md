## Intro
An Ansible module to manage Nuxeo marketplace packages. See the playbook marketplace_example.yaml for usage example.

## Getting Started
Simply run 'vagrant up' to get started with a Ubuntu VM with Ansible installed. The provisioning script will execute the example playbook.

## Example Output:

```
$ ansible-playbook package_example.yml -i 'localhost,' --connection=local

PLAY [nuxeo marketplace package] **********************************************

TASK: [install nuxeo-drive] ***************************************************
changed: [localhost]

TASK: [check install idempotency] *********************************************
ok: [localhost]

TASK: [remove nuxeo-drive] ****************************************************
changed: [localhost]

TASK: [check remove idempotency] **********************************************
ok: [localhost]

PLAY RECAP ********************************************************************
localhost                  : ok=4    changed=2    unreachable=0    failed=0

```
