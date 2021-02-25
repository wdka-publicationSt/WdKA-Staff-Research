for cover in ./*.pdf; do
  gs \
    -o "${cover%.pdf}-resampled-gray.pdf" \
    -sDEVICE=pdfwrite \
    -sProcessColorModel=DeviceGray \
    -sColorConversionStrategy=Gray \
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
    "${cover}"

  rm "${cover}";
  mv "${cover%.pdf}-resampled-gray.pdf" "${cover}";

  # Set mediaboxes using mutool
  mutool run setMediaBoxCover.js "${cover}";
done