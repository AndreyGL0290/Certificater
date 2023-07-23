#!/bin/sh

DATE=$(date "+%d.%m.%Y")

libreoffice --headless --invisible --convert-to pdf --outdir ./GENERATED_PDF/$DATE ./GENERATED_PPTX/$DATE/*.pptx
