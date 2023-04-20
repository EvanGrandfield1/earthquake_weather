# main.py
import sys
from earthquakes import earthquake

def main():
    args = sys.argv[1:]
    
    # 1. Check for the arg pattern:
    #   python3 main.py -n 3
    #   e.g. args[0] is '-n' and args[1] is an int
    if len(args) == 2 and args[0] == '-n':
        n = args[1]
        earthquake(n=n)

if __name__ == "__main__":
    main()
