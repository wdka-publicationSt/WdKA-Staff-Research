# WdKA STAFF RESEARCH 2019

Process page <http://publicationstation.wdka.hro.nl/wiki/index.php/Publisher:WdKA_Staff_Research_Publication>

## conversion
To convert the .docx files in the docx/ folder to either html or icml:

* open terminal
* write `cd ` and drag-and-drop this folder into it.

* run `./make.py html` for html output
* run `./make.py --to icml` for icml output
* run `./make.py --to website` for website output



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
