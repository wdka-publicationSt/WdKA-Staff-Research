# Processes all pdf files in this folder sets correct media boxes

# Set correct DPI in images
gs \
  -o publication-resampled.pdf \
  -sDEVICE=pdfwrite \
  -dDownsampleColorImages=true \
  -dDownsampleGrayImages=true \
  -dDownsampleMonoImages=true \
  -dColorImageResolution=300 \
  -dGrayImageResolution=300 \
  -dMonoImageResolution=300 \
  -dColorImageDownsampleThreshold=1.0 \
  -dGrayImageDownsampleThreshold=1.0 \
  -dMonoImageDownsampleThreshold=1.0 \
  -dAutoRotatePages=/None \
   publication.pdf

# Color conversion
# Based on OSP's pdfutils: https://gitlab.constantvzw.org/osp/tools.pdfutils
# CONVERTS RGB PDF TO CMYK PDF PRESERVING TRUE BLACK FOR VECTORS
gs -q -sDEVICE=pdfwrite -o publication-CMYK.pdf -sColorConversionStrategy=CMYK -sSourceObjectICC=control.txt publication-resampled.pdf

rm publication-resampled.pdf

# Set mediaboxes using mutool
mutool run setMediaBox.js publication-CMYK.pdf