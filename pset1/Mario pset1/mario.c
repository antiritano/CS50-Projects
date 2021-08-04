#include <stdio.h>
#include <cs50.h>

int main(void)
{

    int height;

    do
    {
        //User Input
        height = get_int("Height of Pyramid?");
    }

    while (height < 1 || height > 8);

    for (int hash = 0; hash < height; hash++)
    {
        //Spaces
        for (int space = height - 1; space > hash; space--)
        {
            printf(" ");
        }

        //hashes
        for (int space = 0; space <= hash; space++)
        {
            printf("#");
        }

        printf("\n");





    }

}