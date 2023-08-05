import shutil
import os

def inspect():

    print("inspecting malicious.jar")
    inspect_folder("temp")

    print("removing temp directory")
    shutil.rmtree("temp")

def inspect_folder(dir):
    for root, dirs, files in os.walk(dir):
        for file in files:
            try:
                inspect_file(os.path.join(root, file))
            except Exception as e:
                print("error inspecting file: " + str(e) + " " + os.path.join(root, file))
        for dir in dirs:
            inspect_folder(os.path.join(root, dir))

def inspect_file(path):
    if path.endswith("Hooks347.class"):
        print("found malicious class file: " + path)
    
    lines = []
    with open(path, "r") as f:
        lines = f.readlines()

    for line in lines:
        if "discord" in line.lower():
            print("found discord reference: " + line)
        if "token" in line.lower():
            print("found token reference: " + line)
        if "webhook" in line.lower():
            print("found webhook reference: " + line)