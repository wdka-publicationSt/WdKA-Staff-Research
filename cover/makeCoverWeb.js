/**
 * Generate a front and back cover, based on the cover generated for print.
 * 
 * Copy over the single page from the print cover twice and set the page boxes
 * to reveal only the right (front) and left (back) side.
 */

function mm (val) {
  return val / 0.352777778
}

function copyPage(dstDoc, srcDoc, pageNumber, dstFromSrc) {
  var srcPage, dstPage
  srcPage = srcDoc.findPage(pageNumber)
  dstPage = dstDoc.newDictionary()
  dstPage.Type = dstDoc.newName("Page")
  if (srcPage.MediaBox) dstPage.MediaBox = dstFromSrc.graftObject(srcPage.MediaBox)
  if (srcPage.Rotate) dstPage.Rotate = dstFromSrc.graftObject(srcPage.Rotate)
  if (srcPage.Resources) dstPage.Resources = dstFromSrc.graftObject(srcPage.Resources)
  if (srcPage.Contents) dstPage.Contents = dstFromSrc.graftObject(srcPage.Contents)
  dstDoc.insertPage(-1, dstDoc.addObject(dstPage))
}

var pageWidth = mm(148),
    spineWidth = mm(8.56),
    pageHeight = mm(210),
    slugLength = mm(5), // max(cropmarklength + cropmarkOffset, bleed)
    cropMarkLength = mm(1.5),
    bleed = mm(3),
    doc = new PDFDocument(argv[1]),
    dstDoc = new PDFDocument(),
    dstFromSrc = dstDoc.newGraftMap();

/**
 * Copy over the single page from the original cover to the new file
 */
copyPage(dstDoc, doc, 0, dstFromSrc);
copyPage(dstDoc, doc, 0, dstFromSrc);

var coverFront = dstDoc.findPage(0),
    coverBack = dstDoc.findPage(1);

coverFront.MediaBox = coverFront.CropBox = coverFront.TrimBox = coverFront.BleedBox = [
  slugLength + pageWidth + spineWidth,              // Bottom left X
  slugLength,                                       // Bottom left Y
  slugLength + pageWidth + spineWidth + pageWidth, // Top right X
  slugLength + pageHeight                           // Top right Y
];

coverBack.MediaBox = coverBack.CropBox = coverBack.TrimBox = coverBack.BleedBox = [
  slugLength,                                       // Bottom left X
  slugLength,                                       // Bottom left Y
  slugLength + pageWidth,                           // Top right X
  slugLength + pageHeight                           // Top right Y
];

dstDoc.save(argv[2]);