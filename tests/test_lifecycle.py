from pathlib import Path
import unittest
import yaml
ROOT=Path(__file__).resolve().parents[1]
class AnsibleContractTests(unittest.TestCase):
    def test_serial_rollout_prevents_fleetwide_restart(self):
        p=yaml.safe_load((ROOT/'playbooks/site.yml').read_text())[0]
        self.assertEqual(1,p['serial'])
        self.assertTrue(p['any_errors_fatal'])
        self.assertIn('pre_tasks',p)
    def test_production_change_requires_approval(self):
        p=(ROOT/'playbooks/preflight.yml').read_text()
        self.assertIn('approve_production_configuration',p)
    def test_no_static_private_keys_are_committed(self):
        for file in ROOT.rglob('*'):
            if not file.is_file() or '.git' in file.parts or '.lab' in file.parts:continue
            if file.suffix in ('.pem','.key'):self.fail(f'Secret-like file: {file}')
    def test_nginx_verification_is_active(self):
        p=(ROOT/'playbooks/verify.yml').read_text()
        self.assertIn('nginx -t',p)
        self.assertIn('http://127.0.0.1/health',p)
    def test_inventory_hosts_match_compose(self):
        c=yaml.safe_load((ROOT/'docker-compose.yml').read_text())
        inv=yaml.safe_load((ROOT/'inventories/dev/hosts.yml').read_text())
        self.assertTrue(set(inv['all']['children']['linux_servers']['hosts']).issubset(c['services']))
if __name__=='__main__':unittest.main()
