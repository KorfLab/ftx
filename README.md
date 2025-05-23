Kompressed Genomic Features
===========================

This repo describes the Kompressed Genomic Features (.kgf) file format. It
simplifies the description of some complex genomic entities like genes.

## Quick Start ##

Examine the genomic locus below.

- Low complexity region (LC) from 5-15
- Gene (gene-x) from 17-65 with 2 isoforms
	- tx-1 is spliced with start at 22
	- tx-2 is unspliced with a start at 32

```
ACGTAAAAAAAAAACGTACGTATGATAGCGAATGTAGGAGATTTCAGAAAAGGTTTTATAACACGATCAT
^        ^         ^         ^         ^         ^         ^         ^
1        10        20        30        40        50        60        70
    <---LC--->
                 <----------------------------------------------> gene-x

                 5555MetIleAlaAsn--------------LysArgPhe***333333
                 <-----Exon-----><---Intron---><------Exon------> tx-1

                 55555555555555MetTrpGluLysSerGluLysValLeu***3333
                 <---------------------Exon---------------------> tx-2
```

Describing this in GFF is verbose and confusing (note that this isn't exactly
GFF3, which is tab-delimited, but it's easier to read with the padding).

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

Describing this in KGF is much more compact and has several conveniences that
make it much more intuitive and useful for human readers. The location is the
first field, and this is copy-pastable into genome browsers. The relative
coordinates in field 4 allow one to think about the size of the locus without
enormous genomic coordinates. The name follows a simple and intuitive
directory/file scheme for nested features.

```
# KGF
chr1:5-14|re|.|1-10|.|low-complexity
chr1:17-65|tx|+4|1-20,31-48|.|gene-x/tx-1
chr1:17-65|tx|+14|1-48|.|gene-x/tx-2
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

Like GFF3, the type of a feature comes from the Sequence Ontolgy. In addition,
some types are used so frequently that they have digram aliases. These are
described below.

- `cd` coding_region_of_exon
- `ex` exon
- `in` intron
- `re` repeat_region
- `tx` transcript
- `u5` five_prime_utr
- `u3` three_prime_utr

KGF digrams also include some things that are not in SO.

- `ns` nucleotide similarity
- `ps` protein similarity



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

Features are named somewhat like a `directory/file` hierarchy. Directories do
not need to be unique, but the `directory/file` token must be. This naming
scheme allows one to give features generic or specific names.

All `tx` features must specify both their gene name and transcript name as:
`gene-name/unique-transcript-name`

Features other than `tx` may also use the `directory/file` naming convention.


## Philosophy ##

One of the strengths of GFF is that it is line based, and therefore works with
typical command line programs like `grep` and `perl`. The main problem with
this is that line-based formats make it difficult to capture hierarchical
structures. For example, genes are composed of transcripts, and transcripts are
composed of exons, and possibly introns, start and stop codons, CDSs and UTRs.
This multi-layered structure is difficult to visualize across multiple lines
with many redundant text fields. We therefore sought to create a line-based
format that also encapsulates gene structure.

The location is specified as `chr:begin-end` because this format is used in
genome browsers. Being able to copy-paste the chromosome coordinate token into
genome browsers is a big time-saver.

There is a lot of redundant text in GFF.

In GFF, the positions of introns are often left out because one can always
infer them from the positions of exons. KGF takes this a step further. Given
exons and a start codon, it's possible to infer CDS, intron, and UTR.

Unlike GFF, KGF does not explicitly specify gene features. A gene is defined by
its collection of transcripts and its position can be inferred from the extent
of those transcripts. The gene name is embedded in each transcript as their
parent _folder_. This is both simple and intuitive.



lost
individual scores
indifiviual sources
