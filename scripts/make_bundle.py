import os
import zipfile

SRC = "dist"
OUT = "site-bundle.zip"

if os.path.exists(OUT):
    os.remove(OUT)

count = 0
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for root, _dirs, files in os.walk(SRC):
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, SRC).replace(os.sep, "/")
            z.write(full, rel)
            count += 1

with zipfile.ZipFile(OUT) as z:
    names = z.namelist()
    bad = [n for n in names if "\\" in n]
    print(f"{len(names)} files, root index.html: {'index.html' in names}, backslashes: {len(bad)}")
    for n in names:
        print(" ", n)
print(f"OK: wrote {OUT} ({count} files)")
