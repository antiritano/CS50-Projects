#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// Get the key to the encryption
int main(int argc, string argv[])
{
    string key = argv[1];
    if (argc != 2)
    {
        printf("Enter a valid Key");
        return 1;
    }
    else
    {
        // Convert the string to an integer
        int k = atoi(key) % 26;
        
        // Check the key is valid
        if (k == 0)
        {
            printf("Invalid key. Try again");
            return 1;
        }
    
        // Get the text from the user to encrypt
        string text = get_string("Insert Text:");
        if (text != NULL)
        {
    
            // Encrypt and print
            printf("ciphertext:");
            for (int i = 0, n = strlen(text); i < n; i++)
            {
                int c = 0;    
        
                // Check if text is upper or lower 
             
                if (isupper(text[i]))
                {
                   
                    c = (((int)text[i] - 65 + k) % 26) + 65;
                    printf("%c", (char) c);
                }
                else if (islower(text[i]))
                {
                    
                    c = (((int)text[i] - 97 + k) % 26) + 97;
                    printf("%c", (char) c);
                }
                else
                {
                    printf("%c", text[i]);
                }
            }
            printf("\n");
            return 0;
        }
    }
}