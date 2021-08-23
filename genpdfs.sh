#!/bin/bash

# sudo apt-get install wkhtmltopdf
for filename in html-alunos/*.html; do
    wkhtmltopdf -q $filename pdfs/$(basename "$filename" .html).pdf
    echo $(basename "$filename" .html) "feito!"
done
