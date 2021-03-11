# Reduce to 150 dpi.
# Set media boxes to hide crop marks on the body
# Run script for the cover to double the pages,
# with a media box for the front and back cover

# Reduce DPI to 150
gs \
  -o publication-web-resampled.pdf \
  -sDEVICE=pdfwrite \
  -dDownsampleColorImages=true \
  -dDownsampleGrayImages=true \
  -dDownsampleMonoImages=true \
  -dColorImageResolution=150 \
  -dGrayImageResolution=150 \
  -dMonoImageResolution=150 \
  -dColorImageDownsampleThreshold=1.0 \
  -dGrayImageDownsampleThreshold=1.0 \
  -dMonoImageDownsampleThreshold=1.0 \
  -dAutoRotatePages=/None \
   publication.pdf

# Set mediaboxes on content using mutool
mutool run setMediaBoxWeb.js publication-web-resampled.pdf

# Double the cover and set mediaboxes to show front and back
mutool run ../cover/makeCoverWeb.js ../cover/cover3.pdf ./cover-web.pdf;

# Combine cover and content
pdftk A=cover-web.pdf B=publication-web-resampled.pdf cat A1 B A2 output publication-web.pdf

rm cover-web.pdf publication-web-resampled.pdf