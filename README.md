Kompressed Genomic Features
===========================

This repo describes the Kompressed Genomic Features (.kgf) file format. It
simplifies the description of some complex genomic entities like genes.

## Quick Start ##

Imagine the genomic locus below. It has a low-complexity region and a
protein-coding gene with 2 alternative isoforms, one of which has an intron.

```
ACGTAAAAAAAAAACGTACGTATGATAGCGAATGTAGGAGATTTCAGAAAAGGTTTTATAACACGATCAT
^        ^         ^         ^         ^         ^         ^         ^
1        10        20        30        40        50        60        70

    xxxxxxxxxx   5555MetIleAlaAsn------------AGLysArgPhe***333333
    <---lc--->   <-----Exon-----><---Intron---><------Exon------> tx1

                 55555555555555MetTrpGluLysSerGluLysValLeu***3333
                 <---------------------Exon---------------------> tx2
```

Describing this in GFF is verbose and confusing (yeah, this isn't exactly GFF3,
but it's easier to read with padding).

```
# GFF3-ish
chr1 src low_complexity   5 15 . . .
chr1 src gene            17 65 . + . ID=gene-x
chr1 src mRNA            17 65 . + . ID=tx-1 Parent=gene-x
chr1 src five_prime_utr  17 20 . + . Parent=tx-1
chr1 src exon            17 33 . + . Parent=tx-1
chr1 src cds             22 33 . + 0 Parent=tx-1
chr1 src intron          34 47 . + . Parent=tx-1
chr1 src cds             48 59 . + 0 Parent=tx-1
chr1 src exon            48 65 . + . Parent=tx-1
chr1 src three_prime_utr 60 65 . + . Parent=tx-1
chr1 src mRNA            17 65 . + . ID=tx-2 Parent=gene-x
chr1 src five_prime_utr  17 31 . + . Parent=tx-2
chr1 src exon            17 65 . + . Parent=tx-2
chr1 src cds             32 63 . + 0 Parent=tx-2
chr1 src three_prime_utr 60 63 . + . Parent=tx-2
```

Describing this in KGF is much more compact and easier to read even without
whitespace delimiters.

```
# KGF
I:5-14|re|.|1-10|.|low-complexity
I:17-65|tx|+4|1-20,31-48|.|gene-x/tx-1
I:17-65|tx|+14|1-48|.|gene-x/tx-2
```

## Specification ##

- Lines beginning with a hash symbol, `#`, are comments
- The field delimeter is the pipe symbol, `|`
- Coordinates are all 1-based
- There are 6 mandatory fields, none of which allow whitespace:
  - Location - `chr:beg-end`
  - Type - a controlled vocabulary of digrams
  - Strand - plus or minus and offset for coding sequences, . for none
  - Structure - describes spans `beg-end` and intevals `beg-end,beg-end`
  - Score - a dot is used when there is no score
  - Name - allows generic and unique ids, gene names are like folders

### Location

The location of a feature has 3 parts: chromosome, beginning coordinate, and
ending coordinate: `chr:beg-end`. The begin is always smaller than the end. The
location string matches the common standard used in genome browsers, and is
therefore an easy copy-paste for viewing.

### Type

The type of a feature is a digram from a controlled vocabulary. The most
important Type is `tx`, which is used for transcripts. This encapsulates exons,
introns, CDSs and UTRs. However, if you want to specify individual components,
you can.

- `tx` transcript
- `ex` exon
- `in` intron
- `aa` coding sequence
- `u5` 5' UTR
- `u3` 3' UTR
- `re` repetitive element
- `sa` sequence alignment


### Strand

The strand is a single character, either a plus or minus, optionally followed
by a number. For non-stranded features, like a low-complexity region, strand is
left blank. For transcripts that are translated, the distance from the 5' end
to the start codon is given after the strand indicator.

### Structure

The structure field is used to describe the feature in relative coordinates.
For features that are split, combine with commas.

### Score

Score is an abitrary numeric field.

### Name

The name of a feature may be unique or generic. Unique names are used for
features like gene names. Generic feature names are used as sub-classifiers of
type. For example, a repetitive element may have a sub-class as Alu.


## Philosophy ##

One of the strengths of GFF is that it is line based, and therefore works with
typical command line programs like `grep` and `perl`. The main problem with
this is that line-based formats make it difficult to capture nested structures.
For example, genes are composed of transcripts, and transcripts are composed of
exons, and possibly introns, CDSs and UTRs. This multi-layered structure is
difficult to visualize across multiple lines with many redundant text fields.
We therefore sought to create a line-based format that also encapsulates gene
structure.

In GFF, the positions of introns are often left out, because one can always
infer them from the positions of exons. KGF takes this a step further. Given
exons and a start codon, it's possible to infer CDS, intron, and UTR.

KGF does not explicitly specify gene features. A gene is defined by its
collection of transcripts and its position can be inferred from the extent of
those transcripts. The gene name is embedded in each transcript as the parent
_folder_.

The location is specified as `chr:begin-end` because this format is used in
genome browsers. It's convenient to be able to copy-paste the chromosome
coordinate token into genome browsers.



- If one knows the position of the start codon, one can infer CDS and UTR
- The parent child relationships of transcripts to genes is folder-esque


