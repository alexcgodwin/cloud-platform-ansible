"""Reject second-run Ansible recap that reports any changed/failed/unreachable hosts."""
import re,sys
from pathlib import Path

def is_idempotent(log: str) -> bool:
    chunks=log.split('PLAY RECAP')
    if len(chunks)<2:return False
    recap=chunks[-1]
    hosts=re.findall(r'^([\w.-]+)\s*:\s*ok=\d+\s+changed=(\d+)\s+unreachable=(\d+)\s+failed=(\d+)', recap, re.MULTILINE)
    return len(hosts)>=2 and all((int(c)==0 and int(u)==0 and int(f)==0) for _,c,u,f in hosts)

if __name__=='__main__':
    if len(sys.argv)!=2 or not is_idempotent(Path(sys.argv[1]).read_text(encoding='utf-8')):
        raise SystemExit('Second Ansible run changed resources or failed. Investigate drift.')
    print('Idempotency verified: no managed-node changes on second pass')
