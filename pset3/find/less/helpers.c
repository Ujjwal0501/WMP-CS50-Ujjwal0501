/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */

#include <cs50.h>
#include <math.h>
#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    // searching algorithm
    if (n > 1)
    {
        if (value != values[n / 2] && (value > values[n / 2]))
        {
            if (search(value, &values[n / 2], round(n / 2.0)))
            {
                return true;
            }
        }
        else if (value != values[n / 2] && (value < values[n / 2]))
        {
            if (search(value, values, n / 2))
            {
                return true;
            }
        }
        else
        {
            return true;
        }
    }
    else
    {
        if (value == values[0])
        {
            return true;
        }
        else
        {
            return false;
        }
    }
    // return false;
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    // sorting using selection sort
    int i, j;
    for (i = 0; i < n - 1; i++)
    {
        for (j = i + 1; j < n; j++)
        {
            if (values[i] > values[j])
            {
                int temp = values[j];
                values[j] = values[i];
                values[i] = temp;
            }
        }
    }
    return;
}
