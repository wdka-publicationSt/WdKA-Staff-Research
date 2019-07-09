# WdKA STAFF RESEARCH 2019

Process page <http://publicationstation.wdka.hro.nl/wiki/index.php/Publisher:WdKA_Staff_Research_Publication>

## Depencies:
* Pandoc <http://pandoc.org/>
* Python libraries:
    - Jinja2
        + website: http://jinja.pocoo.org/
        + install: `pip3 install Jinja2`
    - PyYAML
        + website: <https://pyyaml.org/wiki/PyYAMLDocumentation>    
        + install: `pip3 install pyyaml`
    - NLTK (for `./make wordfrequency`)
        + website: <https://www.nltk.org>
        + install setps:
            + install nltk : `pip3 install --user -U nltk`
            + run python interpreter `python3`
            + import NLTK `import nltk` if python does not complain you are good :)
            + now it is time to download some the NLTK packages we need
                + `nltk.download('stopwords')` to exclude English stopwords
                + `nltk.download('punkt')` to tokenize the text's sentences
            + You are done installing. Exit python: `exit()` 
## Metadata
`publication_metadata.yaml` includes 
* metadata about the publication
*  Table Of Contents (TOC): 

The information contained in this file is used to generate the structure of the publication and its colophone.

## conversion
To convert the .docx files in the docx/ folder to either html, icml or website:

* open terminal
* write `cd ` and drag-and-drop this folder into it.

* run `./make.py html` for html output
* run `./make.py icml` for icml output
* run `./make.py website` for website output
    - website styling is defined in: `website/style.css` as its stylesheet
    - resulting website will be saved in folder `website/` 
* run `./make.py pdf` for PDF output
    - PDF styling is defined in: `pdf/style.pdf.css` as CSS
    - errors found while generating the pdf are stored in `pdf/weasyprint.log`
    - resulting pdf will be saved in `pdf/publication.pdf`
* run `./make.py  wordfrequency` to get the texts' word frequency


## On CSS for print
[W3C page on CSS Paged Media](https://www.w3.org/TR/css-page-3/) describest in detail: *how pages are generated and laid out to hold fragmented content in a paged presentation*, such as page margins, page size and orientation, headers and footers, page numbering and running headers / footers.

[W3C page on CSS Fragmentation Module](https://www.w3.org/TR/css-break-3/#breaking-controls) explains in detail how page breaks are controlled in CSS.

```
FOLDER STRUCTURE
├─ convert.py
├─ createhtml.py
├── docx (source texts: docx)
│   └──  ....
├── html (converted html)
│   └── ...
├── icml (converted icml)
├─ publication_metadata.yaml
├── README.md
├─ readyaml.py
├── website (website content + structure)
│   └── ...
└── website-templates
    ├── base.html
    ├── contentpage.html
    ├── menu.html
    └── style.css
```

## On images on docx
Because when the images in a docx file are converted by Pandoc they are given a default source and loose their descriptions we devised a different strategies for including images in a word document.

In the word document you include the image as a reference using the follwoing syntax:
`![figure caption](image path)`

As for instance:
`![BluecityLab - Intern Lieke van der Maas working with Kombucha http://www.bluecitylab.nl/](images/AldjevanMeer/bluecitylab.png)`

Ensure that:
* **there is no formatting on that line of text**
* **it is seperate from other text lines with a empty line before and after**

The result, when converted to an HTML will be:
```html
<figure>
    <img src="../images/AldjevanMeer/bluecitylab.png">                  
    <figcaption>BluecityLab - Intern Lieke van der Maas working with Kombucha<a href="http://www.bluecitylab.nl/"><span class="underline">http://www.bluecitylab.nl</span></a>/</figcaption>
</figure>
```