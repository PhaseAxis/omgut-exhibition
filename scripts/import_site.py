import base64, hashlib, io, json, pathlib, zipfile
root = pathlib.Path("public")
root.mkdir(exist_ok=True)
manifest = json.loads(pathlib.Path("migration-manifest.json").read_text())
parts = sorted(pathlib.Path(".migration").glob("part-*.txt"))
archive = zipfile.ZipFile(io.BytesIO(base64.b64decode("".join(p.read_text() for p in parts), validate=True)))
for name, expected in manifest.items():
    target = root / name
    if target.exists():
        continue
    data = archive.read(name)
    if hashlib.sha256(data).hexdigest() != expected:
        raise RuntimeError("Checksum mismatch: " + name)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
(root / ".nojekyll").touch()
print("Verified and restored all website files from local archive.")
