#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define BLOCK_SIZE 512

int main(int argc, char **argv)
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "USAGE: ./recover image\n");
        return 1;
    }

    // open image file
    FILE *imgptr = fopen(argv[1], "r");
    if (imgptr == NULL)
    {
        fprintf(stderr, "Unable to open file\n");
        return 2;
    }

    // allocate memory for reading
    unsigned char *fdata = malloc(BLOCK_SIZE);

    int count = -1;
    char *fname  = malloc(9);

    // create output file pointer
    FILE *outptr;

    while (fread(fdata, 1, BLOCK_SIZE, imgptr) == 512)
    {
        // check magic number of jpeg
        if (fdata[0] == 0xff && fdata[1] == 0xd8 && fdata[2] == 0xff && (fdata[3] & 0xf0) == 0xe0)
        {
            if (count != -1)
            {
                // close previous file
                fclose(outptr);
            }

            // count file
            count++;

            // get file name
            sprintf(fname, "%03i.jpg", count);

            // open output image file
            outptr = fopen(fname, "w+");
            if (outptr == NULL)
            {
                fprintf(stderr, "Unable to create file\n");
                return 3;
            }
            fwrite(fdata, 1, BLOCK_SIZE, outptr);
        }
        else
        {
            if (count != -1)
            {
                fwrite(fdata, 1, BLOCK_SIZE, outptr);
            }
        }
    }

    // close image file
    fclose(imgptr);
    free(fdata);
    free(fname);
}