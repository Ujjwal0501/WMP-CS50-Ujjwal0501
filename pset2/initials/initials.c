#include <stdio.h>
#include <cs50.h>
#include <ctype.h>

int main(void)
{
    int i;
    string s1;
    s1 = get_string();
    for (i = 0; s1[i]; i++)
    {
        if (s1[i] != ' ')
        {
            if (i == 0)
            {
                printf("%c", toupper(s1[i]));
            }
            else if (s1[i-1] == ' ')
            {
                printf("%c", toupper(s1[i]));
            }
        }
    }
    printf("\n");
}