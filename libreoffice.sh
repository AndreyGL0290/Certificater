DATE=$(date "+%d.%m.%y")

libreoffice --headless --invisible --convert-to pdf --outdir /GENERATED_PDF/$DATE *.pptx
