#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int count_letters(string sentence);
int count_words(string sentence);
int count_sentence(string paragraph);

int main(void)
{
    //User Input
    string text = get_string("text: \n");
    //Declare Variables
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentence(text);
    //Algorithm
    float s = ((float)sentences / (float)words) * 100;
    float l = ((float)letters / (float)words) * 100;  
   
    float grade = (0.0588 * l) - (0.296 * s) - 15.8;
    int gradeR = round(grade);
    
    //Print Grades
    if (gradeR > 16)
    {
        printf("Grade 16+\n");  
    }
    else if (gradeR < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", gradeR);
    }
}
//Letter Function
int count_letters(string sentence)
{
    
    int letters = 0;
    for (int i = 0, length = strlen(sentence); i < length; i++)
    {
        if (isupper(sentence[i]))
        {
            letters++;
        }
        else if (islower(sentence[i]))
        {
            letters++;
        }
    }
    return letters;
}
//Word Function
int count_words(string sentence)
{
    int words = 0;
    for (int i = 0, length = strlen(sentence); i < length; i++)
    {
        if (isspace(sentence[i]))
        {
            words++;
        }
    }
    
    return words += 1;
}
//Sentence Function
int count_sentence(string paragraph)
{
    int sentences = 0;
    for (int i = 0, length = strlen(paragraph); i < length; i++)
    {
        if (paragraph[i] == '.')
        {
            sentences++;
        }
        if (paragraph[i] == '?')
        {
            sentences++;
        }
        if (paragraph[i] == '!')
        {
            sentences++;
        }
    }
    
    return sentences;
}