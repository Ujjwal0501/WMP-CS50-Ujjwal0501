#include <stdio.h>
#include <string.h>
#include "bmp.h"
#include <stdlib.h>

int main(int argc, char **argv)
{
    // ensure correct usage
    if (argc != 4)
    {
        fprintf(stderr, "USAGE: n input.bmp output.bmp\n");
        return 1;
    }

    // save resize factor
    int n = atoi(argv[1]);

    // open input file
    FILE *inptr = fopen(argv[2], "r");

    // ensure file was open
    if (inptr == NULL)
    {
        fprintf(stderr, "Unable to open file.\n");
        return 2;
    }

    // create output file
    FILE *outptr = fopen(argv[3], "w+");

    // ensure file create was success
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create file\n");
        return 3;
    }

    //read bitmapfileheader
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    //read bitmapinfoheader
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // check valid file format
    if (bi.biCompression != 0 || bf.bfOffBits != 54 || bi.biSize != 40 || bi.biBitCount != 24
        || bf.bfType != 0x4d42)
    {
        fclose(inptr);
        fclose(outptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // changing headerinfo
    bi.biWidth = bi.biWidth * n;
    bi.biHeight = bi.biHeight * n;
    bi.biSizeImage = ((sizeof(RGBTRIPLE) * bi.biWidth) + ((4 - ((bi.biWidth *
                      sizeof(RGBTRIPLE)) % 4)) % 4)) * abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write bitmapfileheader
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write bitmapinfoheader
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // changing headerinfo
    int height, width;
    height = abs(bi.biHeight) / n;
    width = abs(bi.biWidth) / n;

    int i, j, k, padding;
    padding = (4 - (width * sizeof(RGBTRIPLE) % 4)) % 4;

    for (i = 0; i < height; i++)
    {
        for (int l = 0; l < n; l++)
        {
            RGBTRIPLE rgb;
            for (k = 0; k < width; k++)
            {
                // read each pixel
                fread(&rgb, sizeof(RGBTRIPLE), 1, inptr);

                // write each pixel n times
                for (j = 0; j < n; j++)
                {
                    fwrite(&rgb, sizeof(RGBTRIPLE), 1, outptr);
                }
            }

            // write padding in output file
            for (k = 0; k < (4 - ((n * width * sizeof(RGBTRIPLE)) % 4)) % 4; k++)
            {
                fputc(0x00, outptr);
            }

            // seek back to copy n time vertically
            if (l < n - 1)
            {
                fseek(inptr, -(width * sizeof(RGBTRIPLE)), SEEK_CUR);
            }
        }

        // seek the padding in input file
        fseek(inptr, padding, SEEK_CUR);
    }

    // close files
    fclose(inptr);
    fclose(outptr);
}