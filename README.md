KorfLab Genomic Features
========================

This repo formalizes the KorfLab Genomic Features (.kgf) file format we use
that simplifies the description of some complex entities like genes (which are
composed of transcripts) and transcripts (which are composed of exons and
introns).

## Quick Start ##

- How to format the most common thing
- How to validate legal FTX
- How to interchange with GFF3 etc

I:101-300|re|+|1-200|rep1            # repeat sequence
I:101-300|lc|=|1-200|            # low-complexity sequence
I:101-300|tx|+|1-200|            # non-spliced transcript on + strand
I:101-300|tx|-|1-50,151-200|     # spliced transcript on - strand


## Specification ##

- Lines beginning with a hash symbol, `#`, are comments
- The field delimeter is the pipe symbol, `|`
- Coordinates are all 1-based
- There are 5 mandatory fields:
  - Location
  - Type
  - Strand
  - Structure
  - Name
- Whitspace is not allowed in mandatory fields
- There is 1 optional field: info


### Location

The location of a feature is of two formats. `chr` is the name of a chromosome.
Ideally, this matches the identifier in a FASTA file _exactly_. `pos` is used
for a single nucleotide. `beg-end` is used for a coordinate pair where `beg` is
always less than `end`.

- `chr:pos`
- `chr:beg-end`

The location string matches the common standard and is copy-pastable into
genome browsers.

### Type

The type of a feature is described as a digram.

- `lo` low-complexity region
- `re` repetitive element
- `sa` sequence alignment
- `tx` transcript

### Strand

The strand is a single character. When the feature is not stranded, for example
low-complexity sequence, use `=`. Or should this just be blank?

- `+` for plus-strand features
- `-` for minus-strand features
- `=` for strandless features

### Structure

The structure field is used to describe the feature in relative coordinates.
For features that are split, combine with commas.

### Name

Each feature has a name that is unique to the file. Transcript features must
include a gene name akin to a directory path. Do all names have to be unqiue?


### Info

The Info field can be used for several purposes



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

