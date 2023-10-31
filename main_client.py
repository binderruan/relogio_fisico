from relogio_client import Client
import sys

def main(args):
    if len(args) == 1:
        port = int(args[0])
        client = Client(port)
    else:
        print("Usage: python main.py <port>")

if __name__ == '__main__':
    main(sys.argv[1:])
