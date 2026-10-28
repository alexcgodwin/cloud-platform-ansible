# Linux configuration delivery and recovery

## Required preflight

Generate a short-lived SSH key for the isolated Docker lab using `ssh-keygen -t ed25519 -f .lab/ansible_lab -N ''`. Never commit `.lab`. Confirm the inventory, operation scope and approvals before running against non-lab hosts. The lab uses SSH host-key checking disabled, which must **not** be used for production inventories. Establish verified host keys and key lifecycles before production use.

## Delivery gate

`ansible-playbook -i inventories/dev/hosts.yml playbooks/site.yml --syntax-check` validates structure, not deployment. CI generates its own SSH key, runs the two-node Docker lab, verifies HTTP health, repeats the playbook and requires zero changed or failed hosts on the second pass. The playbook applies changes one node at a time, with a preflight check and failure stop.

## Production boundary

The Docker lab's passwordless `sudo` is for disposable nodes only. A production environment must use a dedicated access identity, credential rotation, no global NOPASSWD, verified host keys, approval-gated production inventory and change window. Production must set `approve_production_configuration=true` only through a reviewed operator command.

## Failure recovery

If a configuration change fails, stop further nodes, inspect Ansible task output, `nginx -t`, the health endpoint and changed handlers. Restore the last known-good Git revision after approval, rerun syntax then run playbook with `--check --diff` to inspect potential changes. Avoid automatic rollback that could overwrite emergency repairs. Archive CI artifact and deployment ticket before retry.
