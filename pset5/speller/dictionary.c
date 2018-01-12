/**
 * Implements a dictionary's functionality.
 */

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include "dictionary.h"

// node structure, to load in a trie database
typedef struct node
{
    bool is_word;
    struct node *children[27];
}
node;

// root node not initialized yet, initializing after memory allocation
node *root;
// count of dictionary words
int count = 0;

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    // use diff to remove casing effect
    int i, diff;
    node *temp;
    for (i = 0, temp = root; word[i]; i++)
    {
        diff = isupper(word[i]) ? 65 : 97;

        // separate case for alphabets
        if (isalpha(word[i]))
        {

            if (temp->children[word[i] - diff] == NULL)
            {
                return false;
            }
            else
            {
                temp = temp->children[word[i] - diff];
            }

            // check if word is in dictionary
            if (word[i + 1] == '\0')
            {
                if (temp->is_word)
                {
                    return true;
                }
            }
        }

        // case for apostrophe
        else
        {
            if (temp->children[26] == NULL)
            {
                return false;
            }
            else
            {
                temp = temp->children[26];
            }

            // check if word is present
            if (word[i + 1] == '\0')
            {
                if (temp->is_word)
                {
                    return true;
                }
            }
        }
    }
    return false;
}

// initializer function to silence valgrind error warnings
void init(node *temp)
{
    int i;
    for (i = 0; i < 27; i++)
    {
        temp->children[i] = NULL;
    }
    temp->is_word = false;
}


/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    // open dictionary
    FILE *inptr = fopen(dictionary, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Unable to open dictionary\n");
        return false;
    }

    // prepare to load
    char *word = malloc(52);
    root = malloc(sizeof(node));

    //initialize node members after memory allocation
    init(root);
    while (fscanf(inptr, "%s", word) != EOF)
    {
        node *temp = root;
        for (int i = 0; word[i]; i++)
        {
            tolower(word[i]);
            if (isalpha(word[i]))
            {
                if (temp->children[word[i] - 97] == NULL)
                {
                    // create a new node
                    temp->children[word[i] - 97] = malloc(sizeof(node));
                    temp = temp->children[word[i] - 97];
                    init(temp);
                }
                else
                {
                    // go one level in
                    temp = temp->children[word[i] - 97];
                }
            }
            else
            {
                if (temp->children[26] == NULL)
                {
                    // create a new node
                    temp->children[26] = malloc(sizeof(node));
                    temp = temp->children[26];
                    init(temp);
                }
                else
                {
                    // go one level in
                    temp = temp->children[26];
                }
            }

            // set true at end of word
            if (word[i + 1] == '\0')
            {
                temp->is_word = true;
                count++;
            }
        }
    }
    // close file
    fclose(inptr);

    // free memory
    free(word);
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    // TODO
    return count;
}

// unload using recursive function
void unloadhelper(node *temp)
{
    int i;
    for (i = 0; i < 27; i++)
    {
        if (temp->children[i] != NULL)
        {
            unloadhelper(temp->children[i]);
        }
    }
    free(temp);
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    // TODO
    unloadhelper(root);
    return true;
}
