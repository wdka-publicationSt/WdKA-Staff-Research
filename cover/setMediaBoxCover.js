function mm (val) {
  return val / 0.352777778
}

var pageWidth = mm(148 + 9 + 148),
    pageHeight = mm(210),
    slugLength = mm(5), // max(cropmarklength + cropmarkOffset, bleed)
    cropMarkLength = mm(1.5),
    bleed = mm(3),
    doc = new PDFDocument(argv[1]),
    pageCount = doc.countPages();

for (var i = 0; i < pageCount; i++) {
  var page = doc.findPage(i);
  page.MediaBox = [0, 0, pageWidth + 2 * (slugLength), pageHeight + 2 * (slugLength)]
  page.BleedBox = [slugLength - bleed, slugLength - bleed, pageWidth + (slugLength - bleed) + 2 * bleed, pageHeight + (slugLength - bleed) + 2 * bleed]
  page.TrimBox = [slugLength, slugLength, pageWidth + slugLength, pageHeight + slugLength];
  page.CropBox = page.MediaBox;
}
    
doc.save(argv[1]);