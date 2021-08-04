#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int population;
    int end;
    int years = 0;
    int gain = 0;
    int lose = 0;


    // TODO: Prompt for start size
    do
    {

        population = get_int("Start Size \n") ;
    }
    while (population < 9);

    // TODO: Prompt for end size

    do
    {
        end = get_int("Ending Size \n") ;
    }

    while (end < population);

    // TODO: Calculate number of years until we reach threshold

    while (population < end)
    {
        gain = population / 3;
        lose = population / 4;
        population = population + gain - lose;
        years++;
    }
    // TODO: Print number of years

    printf("Years: %d\n", years);

}