import hashlib, json, pathlib, urllib.request
root = pathlib.Path("public")
root.mkdir(exist_ok=True)
manifest = json.loads(pathlib.Path("migration-manifest.json").read_text())
for name, expected in manifest.items():
    target = root / name
    if target.exists():
        continue
    url = "https://omgut-research-concept.shukaicao2026.chatgpt.site/" + name
    with urllib.request.urlopen(url, timeout=60) as response:
        data = response.read()
    if hashlib.sha256(data).hexdigest() != expected:
        raise RuntimeError("Checksum mismatch: " + name)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
(root / ".nojekyll").touch()
print("Website files ready; subsequent deployments use repository copies.")
