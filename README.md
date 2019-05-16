# ansible-ops

R@CMON (Monash eResearch Centre) playbooks and roles

## Quick start

A. Install ansible-lint pre-commit hooks

```shell
brew install pre-commit
pre-commit install
```

B. Clone inventory submodule and data.

```shell
git submodule init && git submodule update
```

C. **Optional** install python crypto library to speed up ansible vault actions

```shell
pip install cryptography
```

D. **Optional** install redis for fact caching (defaults to jsonfile atm)

```shell
brew install redis
brew services start redis
pip install redis
export ANSIBLE_INVENTORY_CACHE_PLUGIN=redis
```

1. Setup vault password

   ```shell
   echo XXX > ~/.ansible_vault
   ```

2. Add your own jenkins username & password

   ```shell
   ansible-vault create inventory/prod/group_vars/all/jenkins.yml
   ---
   jenkins_username: XXX
   jenkins_password: XXX
   ```

   Do the same for `ansible-vault create inventory/test/group_vars/all/jenkins.yml`

## Notes

- debugging playbooks

  ```shell
  ansible-playbook --syntax-check
  ansible-playbook --list-hosts #lists valid hosts for a play invocation
  ansible-playbook --check      #predicts changes that may occur
  ansible-playbook --diff       #only works for templates
  ansible-playbook -v/-vvvv     #verbose lvl 1-4
  ansible-lint                  #manually run ansible-lint
  pre-commit run --all-files    #manually run pre-commit hooks
  ```

Set `strategy: debug` on a play to be dropped into a playbook debugger when a playbook fails

## usage/examples:

- install ansible dependencies

  ```shell
  ansible all -m raw -a "apt-get -y install python-dev"
  ```

- patch monash-01 nodes

  ```shell
  ansible-playbook patching.yml -l monash-01
  ```

- patch monash-01 nodes, skipping slack notification and tempest check

  ```shell
  ansible-playbook patching.yml -l monash-01  --skip-tags slack_notification,tempest
  ```

- run security audit on all nodes

  ```shell
  ansible-playbook security_audit.yml
  ```

- run puppet on some nodes (can use a regex)

  ```shell
  ansible "rccomdc3-01*" --become -m puppet
  ```

- update apt cache

  ```shell
  ansible monash-01-compute --become -m command -a 'apt-get update' --become
  ```

- got a list of nodes in fqdn new line delimited?

  ```
  ansible $(sed -e 's/.erc.monash.edu.au//g' nodes.txt | tr '\n' ':') -m ping
  ```

- no fail patching

  ```shell
  ansible monash-01-compute -o -a 'sudo DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" dist-upgrade --allow-downgrades'`
  ```

- working with ansible vars

  ```shell
  ansible db1-02 -m setup | sed '1 s/^.*$/{/' | jq
  ansible rccomdc1r24-07 -m setup | sed '1 s/^.*$/{/' | jq .ansible_facts.ansible_processor
  ```

- puppet dev cycle

1. modify code
2. rsysc with dev server

```shell
ansible-playbook puppetdev.yml -e test_host=<test_target> [-t sync,test to optionally do either]
```
