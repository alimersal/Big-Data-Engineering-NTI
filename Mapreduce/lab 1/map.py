import sys

def main():
    for line in sys.stdin:

        fruits = line.strip().split()
        for fruit in fruits:
            fruit = fruit.strip()
            if fruit:

                print(f"{fruit}\t1")

if __name__ == "__main__":
    main()
