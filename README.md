# paradedup
Find near-duplicates in a text corpus of short documents.

## Installation
```sh
$ pip install git+https://github.com/knit-bee/paradedup.git
```

### Requirements
* Python>=3.8
* datasketch>=1.5
* mmhash3>=3.0

## Usage
```
$ paradedup --help
usage: paradedup [-h] [--output OUTPUT] [--permutations PERMUTATIONS] [--lsh-threshold LSH_THRESHOLD]
                 [--shingle-size SHINGLE_SIZE] [--character-shingle] [--case-insensitive]
                 [--ignore-numbers] [--ignore-whitespace] [--ignore-punctuation]
                 directory

Find near-duplicates among documents by using minhashing and locality-sensitive hashing. See below for
options for minhashing and preprocessing.

positional arguments:
  directory             Directory of files to process

options:
  -h, --help              show this help message and exit
  --output OUTPUT, -o OUTPUT
                          Name of output file to store results of near-duplicate detection. Default is
                          'output.json'.
  --permutations PERMUTATIONS, -p PERMUTATIONS
                          Number of permutations to use for minhashing. Default is 128. This value should
                          be at least 2 and maximal 2**32.
  --lsh-threshold LSH_THRESHOLD, -l LSH_THRESHOLD
                          Threshold for locality sensitive hashing. Takes value between 0.0 and 1.0.
                          Default is 0.9
  --shingle-size SHINGLE_SIZE, -k SHINGLE_SIZE
                          Size of shingles/n-grams for set representation of documents. Default is 3.
  --character-shingle, -s
                          Create shingles/n-grams on character level. If this option is not used, shingles
                          are created on token level which whitespace and word boundary tokenization
                          performed.
  --case-insensitive, -c
                          Convert documents to lowercase.
  --ignore-numbers, -n    Remove digits from documents.
  --ignore-whitespace, -w
                          Strip whitespace characters from documents. This implies the use of --character-
                          shingle.
  --ignore-punctuation, -i
                          Strip punctuation and other special symbols from documents

```


### Example
```sh
$ ls my-dir
file1.txt     
file2.txt     
file3.txt
$ paradedup my-dir -w --lsh-threshold 0.5 --character-shingle
$ cat output.json
{"my-dir/file1.txt": [], "my-dir/file2.txt": [["my-dir/file3.txt", 0.3984375]], "my-dir/file3.txt": [["my-dir/file2.txt", 0.3984375]]}
```


## License
This project is licensed under the GNU General Public License v3.0.
