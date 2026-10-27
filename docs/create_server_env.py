"""Create a fresh server-only Redis secret without displaying it."""
import os
import secrets
from pathlib import Path

target = Path('/home/devops/kr2/.env')
if target.exists():
    raise SystemExit('Existing .env preserved')
fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
with os.fdopen(fd, 'w') as stream:
    stream.write('REDIS_PASSWORD=' + secrets.token_hex(24) + '\n')
os.chown(target, 1001, 1001)
print('Server-only .env created with mode 600')
