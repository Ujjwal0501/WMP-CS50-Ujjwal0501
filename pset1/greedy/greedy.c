#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    double n;
    int count = 0;
    printf("O hai! ");
    do
    {
        printf("How much is owed?\n");
        n = get_double();
    }
    while (n < 0);
    n = round(n * 100 );
    while (n >= 25)
    {
        n -= 25;
        count++;
    }
    while (n >= 10)
    {
        n -= 10;
        count++;
    }
    while (n >= 5)
    {
        n -= 5;
        count++;
    }
    while (n >= 1)
    {
        n -= 1;
        count++;
    }
    printf("%d\n", count);
}