#include <stdio.h>
#include <cs50.h>
#include <string.h>

int main(void)
{
	long long n, i;
	int count = 0, sum = 0;
	do
	{
		printf("Number: ");
		n = get_long_long();
	}
	while (n < 0);
	for (i = n; i > 0; i /= 10)
	{
		sum = sum + i % 10;
		int l = 2 * ((i /= 10) % 10);
		while (l > 0)
		{
			sum = sum + (l % 10);
			l /= 10;
		}
	}
	i = n;
	while (i > 0)
	{
		i /= 10;
		count++;
	}
	if (sum % 10 == 0)
	{
		if (count == 15)
		{
			printf("AMEX\n");
		}
		else if (count == 16 && n / 1000000000000000 == 4)
		{
			printf("VISA\n");
		}
		else if (count == 16 && n / 1000000000000000 == 5)
		{
			printf("MASTERCARD\n");
		}
		else if (count == 13)
		{
			printf("VISA\n");
		}
		else
		{
			printf("INVALID\n");
		}
	}
	else
	{
		printf("INVALID\n");
	}
}