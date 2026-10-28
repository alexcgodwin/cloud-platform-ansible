# Linux Infrastructure Automation with Ansible

A reproducible Linux configuration-management lab that uses Ansible to manage multiple Ubuntu servers over SSH.

## Automation

Ansible configures:

- Linux packages
- Operations user and permissions
- SSH access
- Platform directories
- NGINX
- Server status page
- Health endpoint
- Configuration validation

## Managed Nodes

- node1
- node2

## Validation

The project includes automated configuration and verification playbooks and supports repeat runs for Ansible idempotency testing.

## Configuration governance and release checks

This repository now includes a preflight approval gate, a serial managed-node rollout and automated verification. GitHub Actions creates a fresh SSH key for each disposable two-node Docker lab, applies roles, probes the health endpoints, reruns the configuration and verifies `changed=0` with no unreachable or failed hosts. Ansible syntax checks and repository contract tests also run.

For local integration, generate an untracked `.lab/ansible_lab` and `.lab/ansible_lab.pub` key pair, then use `docker compose build node1 ansible` and `docker compose up -d node1 node2`. Run `docker compose run --rm ansible ansible-playbook -i inventories/dev/hosts.yml playbooks/site.yml`, the verify playbook, then repeat the site playbook. See [operational and security boundaries](docs/OPERATOR_RUNBOOK.md).

The lab uses ephemeral keys, passwordless sudo and disabled SSH host-key verification only for disposable containers. These defaults must **not** be copied into real server fleets. No production system deployment is claimed.
