using OpenCvSharp;
using OpenCvSharp.Text;

Console.Write("Input PDF file: ");
var pdfPath = Console.ReadLine();
pdfPath = string.IsNullOrEmpty(pdfPath) ? "../Samples/sample.pdf" : pdfPath;

const int DPI = 256;
var pdf = PdfDocument.FromFile(pdfPath);

var filePath = pdf.RasterizeToImageFiles(@"./outputs/*.png", PageIndexes: [0], DPI: DPI)[0];

var ocr = new OCR();

ocr.Start(filePath);

partial class OCR
{
    private const string TessData = @"_data/tessdata";

    public void Start(string filePath)
    {
        using var src = new Mat(filePath);
        using var dst = new Mat();

        using (var image = new Mat(filePath))
        using (var tesseract = OCRTesseract.Create(TessData, "eng"))
        {
            tesseract.Run(image, out var outputText, out var componentRects, out var componentTexts, out var componentConfidences);
        }
    }
}