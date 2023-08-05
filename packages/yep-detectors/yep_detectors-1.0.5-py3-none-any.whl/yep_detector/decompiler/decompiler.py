import os

def decompile(path):
    os.rename(path, "malicious.jar")

    if not os.path.exists("decomp.jar"):
        print("decomp.jar does not exist")
        exit(1)

    os.system("java -jar decomp.jar malicious.jar --outputdir temp/")