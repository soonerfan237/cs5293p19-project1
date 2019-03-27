Example of how to run code from the cs5293p19-project1 directory:
pipenv run python project1/main.py --input "otherfiles/*.txt" --input "*.txt" --output "files/" --names --dates --phones --genders --addresses --concept jail --concept kid --stats stdout

The --input command line argument specifies where to get the txt files from.  You can use multiple input arguments to grab files from multiple locations.  For example an input argument of "*.txt" will look at the current directory and grab all files with txt extension.  An input argument of "otherfiles/*.txt" will look for a directory called otherfiles within the current directory and grab any txt files.

The --ouput command line argument specifies the location to store the redacted files.  It will create a folder with the specified name inside the current directory.  It will store the redacted files with the orginal filename but with .redacted extension.

The --stats command line argument specifies how to receive statistics of the redaction process.  The stdout argument will print to stdout.  The stderr argument will print to stderr.  Any other string will generate a file of that name in the parent directory that contains the redation statistics.  The statistics will include the counts of terms of each type redacted per file. There will also be total stats for all documents and term types.

The --names command line argument will detect names and redact them.  To redact terms, the characters will be replaced by X's.  Spaces between words will be kept.  I use the nltk library to find names.  I first tokenize the full text into sentences, then tag the words in the sentences.  Then I chunk the words into concepts.  nltk will tag names with a PERSON tag.  I will redact any words in a PERSON chunk.

The --genders command line argument will detect words that reveal genders and redact them.  To implement this I used regular expressions to detec most gender words, such as him, her, he, she, son, daughter, etc.  Each word will be replaced by X's.

The --phones command line argument will detect phone numbers and redact them.  I used regular expressions to detect common American phone number formats.  It will detect phone numbers with or without an area code.  The area code may be in parentheses or not.  For the main part of the phone number it is looking for 3 numbers followed by a dash and then 4 numbers.

The --dates command line argument will detect many common date formats and redact them.  I used regular expressions to look for formats such as mm/dd/yyyy and m/d/yy and similar formats using slashes.  I also detect dates that use full or abbreviated months (i.e. Jan, Feb, March), optionally with dates.  I also detect days of the week.  Each date term will be redacted and replaced with X's, maintaining spaces between words.

The --addresses command line argument will detect common address formats and redact them.  I used regular expressions to look for series of numbers followed by a word (i.e. street name) and optionally followed by a word corresponding to the type of street (i.e. road, rd, st, way).  Each address will be redacted and replaced with X's, maintaining spaces between words.

The --concept command line argument will detect sentences that are related to the concept specified and redact the entire sentence.  This argument can be used multiple times to provide multiple concepts to redact.  This function uses nltk to find synonyms to the provided word and then find words similar to all of the synonyms.  It will then redact all sentences that contain that set of related words.
