#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int n, i, j;
    do
    {
        printf("Height: ");
        n = get_int();
    }
    while (n > 23 || n < 0);
    for (i = 0; i < n; i++)
    {
        for (j = 1; j < n - i; j++)
        {
            printf(" ");
        }
        for (j = 0; j <= i; j++)
        {
            printf("#");
        }
        printf("  ");
        for (j = 0; j <= i; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}