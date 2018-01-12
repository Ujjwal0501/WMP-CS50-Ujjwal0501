#include <stdio.h>
#include <cs50.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("USAGE: ./caeser k\n");
        return 1;
    }
    int n = 0, i;
    // storing key as integer
    for (i = 0; argv[1][i]; i++)
    {
        n = n * 10 + (int)argv[1][i] - 48;
    }

    //making key smaller
    n %= 26;

    //taking original message from user
    printf("plaintext: ");
    string ptxt = get_string();

    for (i = 0; ptxt[i]; i++)
    {
        //checking if character is alphabet
        if (isalpha(ptxt[i]))
        {
            //encrypting message using key
            if (islower(ptxt[i]))
            {
                ptxt[i] = ((ptxt[i] + n - 122) > 0 ? 96 + (ptxt[i] + n - 122) : ptxt[i] + n);
            }
            else
            {
                ptxt[i] = ((ptxt[i] + n - 90) > 0 ? 64 + (ptxt[i] + n - 90) : ptxt[i] + n);
            }
        }
    }
    printf("ciphertext: %s\n", ptxt);
}