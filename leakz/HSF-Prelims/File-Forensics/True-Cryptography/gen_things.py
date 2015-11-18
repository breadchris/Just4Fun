import os
import random

max_depth = 7
max_folders = 10
max_files = 10
max_file_size = 512

words = []
with open("words", "r") as f:
    words = [x.strip() for x in f.readlines()]

def get_word():
    global words
    return random.choice(words)

def create_files(path):
    for _ in range(0, max_files):
        with open(path + "/" + get_word() + ".something", "w") as f:
            f.write("".join([chr(random.randint(0, 255)) for _ in range(random.randint(100, 1024))]))

def make_folders(path, depth=0):
    if depth == max_depth:
        return
    folder_count = random.randint(0, max_folders)
    folders = []
    for _ in range(folder_count):
        tmp_path = path + "/" + get_word()
        os.mkdir(tmp_path)
        create_files(tmp_path)
        make_folders(tmp_path, depth+1)

make_folders("/home/breadchris/Documents/HSF-Prelims/Disk-OS-Forensics/Encrypted_Containers/fun/")

