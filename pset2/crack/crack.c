#include <stdio.h>
#include <unistd.h>
#include <crypt.h>
#include <cs50.h>
#include <string.h>

//pool of characters and salt
char pool[52] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", salt[3] = {'5', '0', '\0'};

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("USAGE: ./crack hash\n");
        return 1;
    }
    if (strlen(argv[1]) != 13)
    {
        printf("INVALID \'DES hash value\'\n");
        return 1;
    }
    int i;
    //checking 1 character
    for (i = 0; pool[i]; i++)
    {
        char pass[5] = {pool[i], '\0'};
        if(!strcmp(argv[1], crypt(pass, salt)))
        {
            printf("%s\n", pass);
            return 0;
        }
    }
    int j;
    //checking 2 char password
    for (i = 0; pool[i]; i++)
    {
        for (j = 0; pool[j]; j++)
        {
            char pass[5] = {pool[i], pool[j], '\0'};
            if (!strcmp(argv[1], crypt(pass, salt)))
            {
                printf("%s\n", pass);
                return 0;
            }
        }
    }
    int k;
    //checking 3 char password
    for (i = 0; pool[i]; i++)
    {
        for (j = 0; pool[j]; j++)
        {
            for (k = 0; pool[k]; k++)
            {
                char pass[5] = {pool[i], pool[j], pool[k], '\0'};
                if (!strcmp(argv[1], crypt(pass, salt)))
                {
                    printf("%s\n", pass);
                    return 0;
                }
            }
        }
    }
    int l;
    //checking 4 char password
    for (i = 0; pool[i]; i++)
    {
        for (j = 0; pool[j]; j++)
        {
            for (k = 0; pool[k]; k++)
            {
                for (l = 0; pool[l]; l++)
                {
                    char pass[5] = {pool[i], pool[j], pool[k], pool[l], '\0'};
                    if (!strcmp(argv[1], crypt(pass, salt)))
                    {
                        printf("%s\n", pass);
                        return 0;
                    }
                }
            }
        }
    }
}