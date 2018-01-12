import sys
import cs50

def main() :
    if len(sys.argv) != 2 :
        print("USAGE: python caesar.py k")
        return 1

    k = int(sys.argv[1])
    k = k % 26

    # store plaintext
    print("Plaintext: ", end="")
    ptxt = cs50.get_string()
    print("Ciphertext: ", end="")

    ciphertext  = ""
    for i in range(len(ptxt)) :
        if ptxt[i].isupper() :
            if (ord(ptxt[i]) + k - 90) > 0 :
                print(chr(64 + ord(ptxt[i]) + k - 90), end="")
            else :
                print(chr(ord(ptxt[i]) + k), end="")
        elif ptxt[i].islower() :
            if (ord(ptxt[i]) + k - 122) > 0 :
                print(chr(96 + ord(ptxt[i]) + k - 122), end="")
            else :
                print(chr(ord(ptxt[i]) + k), end="")
        else :
            print(ptxt[i], end="")

    print("")

if __name__ == "__main__" :
    main()