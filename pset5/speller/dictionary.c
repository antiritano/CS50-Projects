// Implements a dictionary's functionality
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 65536;

// Hash table
node *table[N];
int wordcount = 0;

node *head = NULL;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int length = strlen(word);
    char copy[length + 1]; 
    copy[length] = '\0'; 
    
    for (int i = 0; i < length; i++) 
    {
        copy[i] = tolower(word[i]);
    }


    int hashcode = hash(copy); 
    node *tmp = table[hashcode]; 
    if (tmp == NULL) 
    {
        return false;
    }

    while (tmp != NULL)
    {
        if (strcasecmp(tmp->word, copy) == 0)
        {
            return true; 
        }

            tmp = tmp->next; 
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO
    unsigned long hash = 5381;

    int c = *word;

    while (c == *word++)
    {
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
    }
    return hash % N;
    
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r"); 
    if (file == NULL) 
    {
        return false;
    }
    {
      
        char buffer[LENGTH + 1];
        while (fscanf(file, "%s", buffer) != EOF) 
        {

            node *n = malloc(sizeof(node)); 
            if (n == NULL) 
            {
        fclose(file);
        
        
        return false;
        }

            else 
            {

                strcpy(n->word,buffer); 

                n->next = NULL; 

                unsigned int index = hash(buffer);

          

                n->next = table[index]; 
                table[index] = n; 

                wordcount++; 
            }
        }
       
       fclose(file);
       
       
       return true;
   }


}


// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return wordcount;
}


bool unload(void)
{
    for (int i = 0; i < N; i++) 
    {
   
        node *tmp1 = table[i]; 
        while (tmp1 != NULL) 
        {
            node *tmp2 = tmp1; 
            tmp1 = tmp1 -> next; 
            free(tmp2); 
        }
    }
   
        return true;
   
}
