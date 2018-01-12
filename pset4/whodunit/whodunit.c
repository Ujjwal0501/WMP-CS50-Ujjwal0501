#include <stdio.h>
#include "bmp.h"
#include <stdlib.h>

int main(int argc, char **argv)
{
    // ensure proper usage
    if (argc != 3)
    {
        fprintf(stderr, "USAGE: ./whodunit clue.bmp verdict.bmp\n");
        return 1;
    }

    // open clue
    FILE *inptr = fopen(argv[1], "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Unable to open clue file\n");
        return 2;
    }

    // create output file
    FILE *outptr = fopen(argv[2], "w+");
    if (outptr == NULL)
    {
        fprintf(stderr, "Unable to create verdict file\n");
        return 3;
    }

    // read headers
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // check if clue is valid BMP
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fprintf(stderr, "Unsupported file format\n");
        return 4;
    }

    // write headers
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    int height = abs(bi.biHeight), width = abs(bi.biWidth), padding, i, j;
    RGBTRIPLE rgb;
    padding = (4 - (width * sizeof(RGBTRIPLE)) % 4) % 4;

    for (i = 0; i < height; i++)
    {
        for (j = 0; j < width; j++)
        {
            // read from clue
            fread(&rgb, sizeof(RGBTRIPLE), 1, inptr);

            // change colors (red and white to black else white)
            if (rgb.rgbtBlue == 0xff && rgb.rgbtGreen == 0xff && rgb.rgbtRed == 0xff)
            {
                rgb.rgbtBlue = 0x00;
                rgb.rgbtRed = 0x00;
                rgb.rgbtGreen = 0x00;
            }
            else if (rgb.rgbtBlue == 0x00 && rgb.rgbtGreen == 0x00 && rgb.rgbtRed == 0xff)
            {
                rgb.rgbtBlue = 0x00;
                rgb.rgbtRed = 0x00;
                rgb.rgbtGreen = 0x00;
            }
            else
            {
                rgb.rgbtBlue = 0xff;
                rgb.rgbtRed = 0xff;
                rgb.rgbtGreen = 0xff;
            }

            // write modified pixel
            fwrite(&rgb, sizeof(RGBTRIPLE), 1, outptr);
        }

        // seek padding of clue
        fseek(inptr, padding, SEEK_CUR);

        // add padding in verdict
        for (int k = 0; k < padding; k++)
        {
            fputc(0x00, outptr);
        }
    }

    // close files
    fclose(inptr);
    fclose(outptr);
}