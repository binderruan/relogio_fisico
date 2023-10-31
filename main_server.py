from relogio_server import Server
import sys

def main(args):
    if len(args) == 1:
        port = int(args[0])
        server = Server(port)
    else:
        print("Usage: python main.py <port>")

if __name__ == '__main__':
    main(sys.argv[1:])
