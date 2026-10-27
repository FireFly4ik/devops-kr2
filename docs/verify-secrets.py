"""Check the delivered project without printing the Redis password."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
values = dict(
    line.split("=", 1)
    for line in (root / ".env").read_text().splitlines()
    if line and not line.startswith("#") and "=" in line
)
password = values.get("REDIS_PASSWORD", "")
if len(password) < 32 or any(c not in "0123456789abcdef" for c in password):
    raise SystemExit("FAIL: password must contain at least 32 hexadecimal characters")
matches = []
for path in root.rglob("*"):
    if path.is_file() and path.name != ".env" and ".git" not in path.parts:
        if password.encode() in path.read_bytes():
            matches.append(str(path.relative_to(root)))
if matches:
    print("FAIL: password found in files:", *matches, sep="\n")
    raise SystemExit(1)
print("OK: random hexadecimal password has at least 32 characters")
print("OK: password not found in delivered files outside .env")
