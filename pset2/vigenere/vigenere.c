#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("USAGE: ./vigenere k\n");
        return 1;
    }
    int i, j;
    //validating key for only alphabets
    for (i = 0; argv[1][i]; i++)
    {
        if (!isalpha(argv[1][i]))
        {
            printf("INVALID key, only alphabets accepted\n");
            return 1;
        }
    }
    //taking message from user
    printf("plaintext: ");
    string ptxt = get_string();
    //encrypting message
    for (i = 0, j = 0; ptxt[i]; i++)
    {
        //encrypting only alphabets
        if (isalpha(ptxt[i]))
        {
            int k = (isupper(argv[1][j]) ? argv[1][j] - 65 : argv[1][j] - 97);
            if (isupper(ptxt[i]))
            {
                ptxt[i] = ((ptxt[i] + k - 90) > 0) ? 64 + ptxt[i] + k - 90 : ptxt[i] + k;
            }
            else
            {
                ptxt[i] = ((ptxt[i] + k - 122) > 0) ? 96 + ptxt[i] + k - 122 : ptxt[i] + k;
            }
            if (j == strlen(argv[1]) - 1)
            {
                j = -1;
            }
            //taking next character in key
            j++;
        }
    }
    printf("ciphertext: %s\n", ptxt);
}