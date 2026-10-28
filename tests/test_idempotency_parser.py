import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from assert_idempotent import is_idempotent
class RecapTests(unittest.TestCase):
    def test_good_recap(self):
        log='PLAY RECAP\nnode1 : ok=12 changed=0 unreachable=0 failed=0 skipped=0\nnode2 : ok=12 changed=0 unreachable=0 failed=0 skipped=0'
        self.assertTrue(is_idempotent(log))
    def test_rejects_changed_resource(self):
        log='PLAY RECAP\nnode1 : ok=12 changed=1 unreachable=0 failed=0\nnode2 : ok=12 changed=0 unreachable=0 failed=0'
        self.assertFalse(is_idempotent(log))
    def test_missing_recap_rejected(self):self.assertFalse(is_idempotent('ok=12 changed=0'))
if __name__=='__main__':unittest.main()
