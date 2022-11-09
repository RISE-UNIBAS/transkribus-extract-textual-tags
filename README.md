# transkribus-export-textual-tags
Python module to extract textual tags from Transkribus PAGE XML to CSV.

## Creator
This software and sample dataset were created by the University of Basel's Research and Infrastructure Support RISE (rise@unibas.ch) in November 2022.

## Quickstart

Export Transkribus PAGE XML documents to a folder and extract the textual tags by running

```
from transkribus_extract_textual_tags.client import Client

Client.extract_from_dir(dir_path="my/transkribus/document/folder",
                        save_file_path="my/output/file.csv"")
```

## License

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.