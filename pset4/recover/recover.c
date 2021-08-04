#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#define BLOCKSIZE 512

//Check for Jpg function
bool isJpgHeader(uint8_t buffer[])
{
    return buffer[0] == 0xff
           && buffer[1] == 0xd8
           && buffer[2] == 0xff
           && (buffer[3] & 0xf0) == 0xe0;
}
int main(int argc, char *argv[])
{
    //Check Command Line Arguments
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }
    char *inputFile = argv[1];
    if (inputFile == NULL)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }
    FILE *inputPointer = fopen(inputFile, "r");
    if (inputPointer == NULL)
    {
        printf("Unable to open file: %s\n", inputFile);
        return 1;
    }
    char filename[8]; // 8 spots including nul  xxx.jpg \0
    FILE *outputPointer = NULL;
    uint8_t buffer[BLOCKSIZE];
    int counter = 0;
  
    while (fread(buffer, sizeof(uint8_t), BLOCKSIZE, inputPointer) || feof(inputPointer) == 0)
    {
        if (isJpgHeader(buffer))
        {  
            if (outputPointer != NULL)
            {
                fclose(outputPointer);
            }
            sprintf(filename, "%03i.jpg", counter);
            outputPointer = fopen(filename, "w");
            counter++;
        
        }
        if (outputPointer != NULL)
        {
            fwrite(buffer, sizeof(buffer), 1, outputPointer);
        }
    }
    //close input file
    if (inputPointer == NULL)
    {
        fclose(inputPointer);
    }
    //close output file
    if (outputPointer == NULL)
    {
        fclose(outputPointer);
    }
    return 0;
}