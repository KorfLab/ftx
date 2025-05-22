KorfLab Genomic Features FTX
============================

This repo formalizes the KorfLab-flavored Fielded Text Format we use to
describe genome sequence features. It's a GFF-adjacent format that simplifies
the description of complex entities like genes (which are composed of
transcripts) and transcripts (which are composed of exons and introns).

This is in a _very_ drafty state

## Quick Start ##

- How to format the most common things
- How to validate legal FTX
- How to interchange with GFF3 etc

chr1|re|a101|+|10-20|
chr1|tx|unc-102/unc-102.1|+|100-200,300-400|
chr1|tx|unc-102/unc-102.1|+|100-200,300-400|


chr1[rs]

chr1|gene-1|+|100-200,300-400,500-600|
chr2|gene-2|-|100-200,300-400,500-600|extra free text
chr1|gene-1|+|100-200,300-400,500-600|~chr1|gene-1|+|100-200,300-400,500-600|


## Specification ##

- Lines beginning with a hash symbol, `#`, are comments
- The field delimeter is the pipe symbol, `|`
- There are 4 mandatory fields: chromosome, annotation, specification, position
- There is 1 final optional field: info

### Chromosome

The chromosome field is used to specify which chromosome the feature is located
on. The name of the chromosome should exactly match the identifier in some
corresponding genome FASTA file. No whitespace is allowed. The pipe symbol is
also not allowed.

### Annotation

The annotation field is a restricted vocabulary of digrams.

- re: repetitive element
- tx: transcript

that corresponds to SO
biological_region

- pseudogene
- 


- gene - holds transcripts
- tx - holds exons, may be coding
- rep
-

| Char | Meaning |
| na
| pa


### Name

Each feature has a name that is unique to the file.

### Strand

The strand for most features is plus or minus. However, some features, like
low-complexity regions are strandless.

- `+` for plus-strand features
- `-` for minus-strand features
- `=` for strandless features


### Coordinates

1-based

Coordinates may be expresed as single numbers, ranges, or intervals

- single numbers correspond to individual nucleotides (e.g. SNP)
- ranges are pairs of begin-end values separated by a dash
- intervals are comma-separated ranges


### Info

The Info field can be used for several purposes

-

Some keys are reserved

- gene - used to show relationship between transcripts and genes
-



## Meta File ##

You will find the official `korflab_genomic_features.ftm` Meta File in the
repo. It is unlikely you will need to use this explicitly.

```
<?xml version="1.0" encoding="utf-16"?>
<FieldedText HeadingLineCount="2" DelimiterChar="|" LineCommentChar="#">
  <Field Name="Chromosome" />
  <Field Name="Type" />
  <Field Name="Name" />
  <Field Name="Strand" />
  <Field Name="Coordinates" />
  <Field Name="Info" />
</FieldedText>
 ```

 It you want to make a Declared Fielded Text file, add this before any of the
 data lines.

 ```
#|!Fielded Text^| Version="1.0"
# MetaEmbedded="True"
# <?xml version="1.0" encoding="utf-16"?>
# <FieldedText HeadingLineCount="2" DelimiterChar="|" LineCommentChar="#">
# <Field Name="Chromosome" />
# <Field Name="Type" />
# <Field Name="Name" />
# <Field Name="Strand" />
# <Field Name="Coordinates" />
# <Field Name="Info" />
# </FieldedText>
```

## Notes ##

https://fieldedtext.org/


## History ##

The SABR project invented a custom record format to serialize gene structure
annotation into a single token for embedding in FASTA/FASTQ identifiers. It was
not intended to be used outside the study, but it proved to be so useful that
we decided to use it more generally as our way of describing genome features.
The original name meant 'flattened transcript format', but it turns out that
the `.ftx` file extension means Fielded Text Format, which is a somewhat
abstract MIME Type for any kind of text file with fields, such as tsv. So it
turns out that the `.ftx` file extension is actually appropriate. The
historical description of the format is as follows:

- file extension: `.ftx`
- field delimiter: `|`
- 5 fields
- no spaces in fields 1-4

1. chromosome identifier
2. name of gene/transcript/read/whatever
3. strand indicator `+` or `-`
4. exon structure:
	- hyphen separated coordinates
	- comma separated exons
	- must be sorted left to right, low to high
	- numbers are 1-based
5. information: optional extra free text

Example: Plus-strand transcript with introns at 201-299 and 401-499 and no
extra information.

```
chr1|gene-1|+|100-200,300-400,500-600|
```

Example: Minus-strand transcript with some extra info.

```
chr2|gene-2|-|100-200,300-400,500-600|extra free text
```

Example: The information field can contain another ftx. This is used within
SABR to attach a genomic source to all of its alignments (an aligner may
provide more than one alignment). A `~` is often used as a delimiter between
ftx elements.

```
chr1|gene-1|+|100-200,300-400,500-600|~chr1|gene-1|+|100-200,300-400,500-600|
```

