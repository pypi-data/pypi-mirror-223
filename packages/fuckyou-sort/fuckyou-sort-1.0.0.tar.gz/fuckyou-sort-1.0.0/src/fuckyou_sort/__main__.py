import sys

from .fuckyou_sort import sort

def main():

    if len(sys.argv) > 1:
        array = sys.argv
        array.pop(0)
        print(array)
        print(sort(array))

if __name__ == "__main__":
    main()