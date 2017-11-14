# calibre-json
Print eBook metadata in JSON format


## Usage

      python2.7 calibre-json.py [-h] [--inline-covers] [--covers-dir dir] file
      calibre-debug calibre-json.py -- [-h] [--inline-covers] [--covers-dir dir] file

    Print eBook metadata in JSON format

    positional arguments:
      file              directory or file to read

    optional arguments:
      -h, --help        show this help message and exit
      --inline-covers   include cover images as base64 data
      --covers-dir dir  directory to store the cover images


## Example

        calibre-debug calibre-json.py -- test/18397.epub

        {
          "rights": "Public domain in the USA.",
          "title": "Socialism and Modern Science (Darwin, Spencer, Marx)",
          "pubdate": "2006-05-15T22:00:00+00:00",
          "file": "18397.epub",
          "path": "test/18397.epub",
          "hash": "3bf493478d9c3ae8f8fa0a1367f3bd1d8252c363af3dc39dcf8e31e7cf195fa5",
          "languages": [
            "eng"
          ],
          "identifiers": {
            "uri": "http://www.gutenberg.org/ebooks/18397"
          },
          "crawl_date": "2017-11-14T18:13:30.020749",
          "cover_data_format": "jpg",
          "authors": [
            "Enrico Ferri"
          ],
          "author_sort": "Ferri, Enrico"
        }
