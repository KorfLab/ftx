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

Describing this in GFF3 is verbose and confusing (note that this isn't exactly
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
first field, and the form is copy-pastable into genome browsers. The relative
coordinates in field 4 allow one to think about the size of the locus without
enormous genomic coordinates and without having to think differently about
genes on the negative strand. The name follows a simple and intuitive
directory/file scheme for nested features like genes and transcipts.

```
# KGF
chr1:5-14|re|.|1-10|.|low-complexity
chr1:17-65|tx|+4|1-20,31-48|.|gene-x/tx-1
chr1:17-65|tx|+14|1-48|.|gene-x/tx-2
```

Similar to GFF-like formats, there is an optional final field that may contain
tag-value information. The format here is `tag=value` with a semicolon
separating multiple tag-value pairs. Again, no spaces are allowed (convert
spaces to underscore).

KGF works well embedded into FASTA file deflines. In this case, omit the
chromosome and begin the record with a colon.

```
>chr1 :17-65|tx|+4|1-20,31-48|.|gene-x/tx-1 :17-65|tx|+14|1-48|.|gene-x/tx-2
ACGTAAAAAAAAAACGTACGTATGATAGCGAATGTAGGAGATTTCAGAAAAGGTTTTATAACACGATCAT
```

## Specification ##

- Lines beginning with a hash symbol, `#`, are comments
- The field delimeter is the pipe symbol, `|`
- Whitespace is forbidden
- Coordinates are all 1-based
- There are 7 fields, the first 6 of which are mandatory
  - Location - `chr:beg-end`
  - Type - a controlled vocabulary of SO terms or digram synonyms
  - Strand - `+`, `-`, or `.` with offset for coding start
  - Structure - describes spans `beg-end` and intervals `beg-end,beg-end`
  - Score - usually a log-odds score or probability, a `.` when unspecified
  - Name - allows hierarchy with `parent/child` relationships
  - Info - `tag=value` separated by semicolons

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

The strand is a single character: `+` for plus strand, `-` for minus strand,
and `.` for unstranded features. The `+` and `-` may be followed by a number.
This is used in transcript features to indicate the length of the 5'UTR. In
other words, it is the offset of the ATG.

### Structure

The structure field is used to describe the feature span as `beg-end` in
coordinates relative to the chromosomal location. The first coordinate always
begins at 1, regardless of strand. For compound features consisting of multiple
`beg-end` pairs, separate with a comma.

### Score

The score field is used to store an arbitrary numeric value. This is usually a
log-odds score but may also be a P-value or E-value. When not specified, use a
`.`. For records that need to record multiple scores, use the Info field.

### Name

Features are named somewhat like a `directory/file` hierarchy. Directories do
not need to be unique, but the `file` token must be. This naming scheme allows
one to give features generic categorizations and specific names. For example, a
repeat feature may be named `Alu` generically or `Alu/AluJ/Alu751` to specify
that the repeat belongs to the Alu family, the AluJ subfamily, and has a
specific name of Alu751 if one wanted to reference it specifically.

All `tx` features must specify both their gene name and transcript name as:
`gene-name/unique-transcript-name`

## Philosophy ##

One of the strengths of GFF is that it is line based, and therefore works with
typical command line programs like `grep` and `perl`. The main problem with
this is that line-based formats make it difficult to capture hierarchical
structures. For example, genes are composed of transcripts, and transcripts are
composed of exons, and possibly introns, start and stop codons, CDSs and UTRs.
This multi-layered structure is difficult to visualize across multiple lines,
especially when those lines may be physically separated by many lines.

There is a lot of redundant text in GFF. While this compresses well, and
therefore doesn't impose a huge overhead in storage, finding interesting
features is akin to looking for a needle in a haystack.

In GFF, the positions of introns are often left out because one can always
infer them from the positions of exons. This concept can be take further: given
exons and a start codon, it's possible to infer CDSs, introns, phases, stops,
and UTRs.

Unlike GFF, KGF does not explicitly specify gene features. A gene is defined by
its collection of transcripts and its position can be inferred from the extent
of those transcripts. The gene name is embedded in each transcript as their
parent _folder_. This is both simple and intuitive.

Genome browsers are an important part of daily life. GFF records don't lend
themselves to easy copy-paste. For this reason, KGF uses the same syntax for
chromosomal locations as genome browsers.

So what does GFF do that KGF does not? There is no explicit _source_ field.
This can be added as `source=whatever` in the info field if you like.
Individual scores of transcript features such as exon scores are not specified
in the more compact `tx` structure. If one wants to label those scores, one can
describe the individual features and their scores. Alternatively, one might use
the info field to aggregate scores such as: `exon_scores=5,3,17`.