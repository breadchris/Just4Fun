
import os, hashlib, zipfile
from shutil import *

voting_sql = "voting_db.sql"
personnel_sql = "personnel.sql"
voting_dir = "voting_versions"
personnel_dir = "personnel_versions"

if not os.path.exists(voting_dir):
    os.makedirs(voting_dir)
if not os.path.exists(personnel_dir):
    os.makedirs(personnel_dir)

voting_file = ""
with open(voting_sql, "r") as f:
    voting_file = f.readlines()

personnel_file = ""
with open(personnel_sql, "r") as f:
    personnel_file = f.readlines()

def sha1(filepath):
    sha = hashlib.sha1()
    with open(filepath, 'rb') as f:
        while True:
            block = f.read(2**10) # Magic number: one-megabyte blocks.
            if not block: break
            sha.update(block)
        return sha.hexdigest()

for i in range(24, len(voting_file), 10):
    with open("out", "w") as f:
        f.write("\n".join(voting_file[0:i]))
    h = sha1("out")
    new_file = "voting_versions/" + h + ".sql"
    move("out", new_file)

for i in range(24, len(personnel_file), 10):
    with open("out", "w") as f:
        f.write("\n".join(personnel_file[0:i]))
    h = sha1("out")
    new_file = "personnel_versions/" + h + ".sql"
    move("out", new_file)

