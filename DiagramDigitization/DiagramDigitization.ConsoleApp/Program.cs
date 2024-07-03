using DiagramDigitization.ConsoleApp;
using PDFiumCore;
using SixLabors.ImageSharp;

fpdfview.FPDF_InitLibrary();

Console.Write("Input PDF file: ");
var pdfPath = Console.ReadLine();

RenderPageToImage(pdfPath);

static void RenderPageToImage(string pdfPath)
{
    double pageWidth = 0;
    double pageHeight = 0;
    float scale = 1;
    // White color.
    uint color = uint.MaxValue;
    // Load the document.
    var document = fpdfview.FPDF_LoadDocument(pdfPath, null);
    var page = fpdfview.FPDF_LoadPage(document, 0);
    fpdfview.FPDF_GetPageSizeByIndex(document, 0, ref pageWidth, ref pageHeight);

    var viewport = new Rectangle()
    {
        X = 0,
        Y = 0,
        Width = (int)pageWidth,
        Height = (int)pageHeight,
    };
    var bitmap = fpdfview.FPDFBitmapCreateEx(
            (int)viewport.Width,
            (int)viewport.Height,
            (int)FPDFBitmapFormat.BGRA,
            IntPtr.Zero,
            0);

    if (bitmap == null)
        throw new Exception("failed to create a bitmap object");

    // Leave out if you want to make the background transparent.
    fpdfview.FPDFBitmapFillRect(bitmap, 0, 0, (int)viewport.Width, (int)viewport.Height, color);

    // |          | a b 0 |
    // | matrix = | c d 0 |
    // |          | e f 1 |
    using var matrix = new FS_MATRIX_();
    using var clipping = new FS_RECTF_();

    matrix.A = scale;
    matrix.B = 0;
    matrix.C = 0;
    matrix.D = scale;
    matrix.E = (float)-viewport.X;
    matrix.F = (float)-viewport.Y;

    clipping.Left = 0;
    clipping.Right = (float)viewport.Width;
    clipping.Bottom = 0;
    clipping.Top = (float)viewport.Height;

    fpdfview.FPDF_RenderPageBitmapWithMatrix(bitmap, page, matrix, clipping, (int)RenderFlags.RenderAnnotations);

    var image = new PdfImage(
        bitmap,
        (int)pageWidth,
        (int)pageHeight);

    Directory.CreateDirectory("outputs");
    image.ImageData.SaveAsPng("outputs/output.png");
}