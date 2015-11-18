
import os, hashlib, zipfile
from shutil import *

if not os.path.exists("release"):
    os.makedirs("release")

printing_flags = False
search_dir = "."
challenges = []

release_dirs = []
for root, dirs, files in os.walk(search_dir):
    for dir in dirs:
        path = os.path.join(root, dir)
        if "release" in dir and path not in ["./release", "./hsfd", "./Judge-Challenges"]:
             release_dirs.append(path)
             break

def zipdir(path, ziph):
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(path)
    for root, dirs, files in os.walk("."):
        for file in files:
            if "challenge_info.txt" not in file:
                ziph.write(os.path.join(root, file))

    os.chdir(cur_dir)

def already_released(chal):
    for root, dirs, files in os.walk("release"):
        for file in files:
            if chal in file:
                return True
    return False

def sha1(filepath):
    sha = hashlib.sha1()
    with open(filepath, 'rb') as f:
        while True:
            block = f.read(2**10) # Magic number: one-megabyte blocks.
            if not block: break
            sha.update(block)
        return sha.hexdigest()

for dir in release_dirs:
    challenge_name = "No challenge name"
    challenge_desc = []
    try:
        chal_info = os.path.join(dir, "challenge_info.txt")
        with open(chal_info, "r") as f:
            challenge_desc = [x.strip() for x in f.readlines()]
            for line in challenge_desc:
                if "Challenge Name: " in line:
                    challenge_name = line[16:].replace(" ", "_").lower()
        if printing_flags:
            with open(os.path.realpath(dir + '/../flag.txt')) as f:
                flag = f.read().strip()
            print challenge_name, flag
        if already_released(challenge_name):
            continue
    except IOError as e:
        print "[-] Make sure the challenge at,", dir, "has a challenge_info.txt ::", e
        continue

    if not printing_flags:
        zip_file = os.path.join("release", challenge_name + "_release.zip")
        z = zipfile.ZipFile(zip_file, "w", allowZip64=True)
        zipdir(dir, z)
        z.close()

        zip_hash = sha1(zip_file)
        new_zip = "release/" + challenge_name + "_" + zip_hash + ".zip"
        move(zip_file, new_zip)
        
        challenges.append([zip_hash + ".zip", challenge_desc])
        print "[+] Challenge:", challenge_name, "added succesfully"

print challenges

