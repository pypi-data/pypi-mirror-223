from decompiler import decompiler
from decompiler import inspector
import argparse

def main():
    parser = argparse.ArgumentParser(description='malicious jar inspector')
    parser.add_argument('jar', type=str, help='path to malicious jar')

    args = parser.parse_args()
    import os
    if not os.path.exists(args.jar):
        print("jar does not exist")
        exit(1)

    decompiler.decompile(args.jar)
    inspector.inspect()

if __name__ == '__main__':
    main()