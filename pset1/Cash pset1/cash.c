#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    
    
    
    float change;
     
    
    do 
    {
        
        //User Input
        change = get_float("How much change is owed?\n");
        
    }
    
    while (change < 0);
    
    
    //Round up change
    int changeR = round(change * 100);
    int coins = 0;    
    //Calculate coins  
    while (changeR >= 25)
    {
        changeR -= 25;
        coins ++;
    }
    
    while (changeR >= 10)
    {
        changeR -= 10;
        coins ++;
    }
    
    while (changeR >= 5)
    {
        changeR -= 5;
        coins ++;
    }
    
    while (changeR >= 1)
    {
        changeR -= 1;
        coins ++;
    }
    
    //Display Coins 
    printf("Coins Owed: ""%i\n", coins); 
    
    
}