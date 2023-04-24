# The `Cain` data format

> A small yet powerful data format

## Index

- [Index](#index)
- [Purpose](#purpose)
  - [Social and economical issue](#social-and-economical-issue)
  - [Environmental issue](#environmental-issue)
- [General Idea](#general-idea)
- [Architecture](#architecture)
  - [Header](#header)
  - [Body](#body)
- [Data encoding](#data-encoding)
  - [Numbers](#numbers)
    - [Integers](#integers)
    - [Floating Point](#floating-point)
  - [Strings](#strings)
    - [Characters](#characters)
      - [Fixed Case Characters](#fixed-case-characters)
      - [Alphanumeric Characters](#alphanumeric-characters)
      - [ASCII Characters](#ascii-characters)
      - [Unicode Characters](#unicode-characters)
  - [Null](#null)
  - [Arrays](#arrays)
  - [Objects](#objects)
  - [Enums](#enums)
- [Data decoding](#data-decoding)
- [References](#references)

## Purpose

In a world where the internet is being used by more than 60% of the population[^1], and with the rise of service APIs to provide users with real-time informations on the fly, data transfers became a major part of our life. Even though most people don't notice it, us developers have the responsibilty to conduct those transfers in the most efficient way possible for several reasons

### Social and economical issue

Even though our internet speeds are becoming faster and faster with technologies such as Optical Fiber and 5G, great inequalities are to be seen worldwide with a non negligible part of consumers still using slow transfer rates technologies such as 3G for availability but also economic reasons.

This brings a huge burden for some countries to develop further as the internet is expected, and already has, a central part in any economic but also public affairs.

With up to 94% of companies now using cloud services and 67% of them having their infrastructure cloud-based, having smaller data storage options may benefit on an economic perspective.

### Environmental issue

While the current environmental footprint of online activites remains arguably low, with the mulitplication of internet users and the more intense usage of the internet in our everyday life, the small environmental impacts add up and become a substantial role in the current environmental issues.

Storage with smaller formats also means a smaller need to allocate resources for databases and data retention.

## General Idea

While formats such as `JSON` and `XML` have big overheads, aiming at both human and machine readable values, most of the time, the data will only be used within a single software are between two softwares, without even being shown once to the end user. Why bother having the human readable part for those use cases ?

Moreover, most data has and should have a fixed schema, which leverages the need to repeat it in the formatted value at the end.

Finally, some data might be redundant and used mutiple times throughout the same file. References can avoid this by simply writing the data once and reference to it in the right fields. While this might be avoided with JSON using compression algorithms (which should definitely be used), this helps reduce uncompressed sizes, for browsers which don't support some compression algorithms yet, use cases outside of web development and performance critical environments.

This format aims at bringing the smallest data formatting possible for machine-to-machine communications by avoiding any redundancy and unnecessary syntax.

## Architecture

### Header

### Body

## Data encoding

### Numbers

#### Integers

#### Floating Point

### Strings

Strings are just arrays of fixed length characters

They generally end with a null `\0` byte.

#### Characters

To optimize the size taken by characters, we can have them encoded different ways.

##### Fixed Case Characters

*Fixed Case* characters take 5 bits, which gives $2^5 = 32$ different entries.

We can specify the case for the characters.

| Character | `NULL` | `A` | `B` | `C` | `D` | `E` | `F` | `G` | `H` | `I` | `J`  | `K`  | `L`  | `M`  | `N`  | `O`  | `P`  | `Q`  | `R`  | `S`  | `T`  | `U`  | `V`  | `W`  | `X`  | `Y`  | `Z`  | `SPACE` | `NEWLINE` | `TAB` |
| --------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | --- | --- | --- |
| Value    | `0`    | `1` | `2` | `3` | `4` | `5` | `6` | `7` | `8` | `9` | `10` | `11` | `12` | `13` | `14` | `15` | `16` | `17` | `18` | `19` | `20` | `21` | `22` | `23` | `24` | `25` | `26` | `27` | `28` | `29` |

##### Alphanumeric Characters

| Character | `NULL` | `A` | `B` | `C` | `D` | `E` | `F` | `G` | `H` | `I` | `J`  | `K`  | `L`  | `M`  | `N`  | `O`  | `P`  | `Q`  | `R`  | `S`  | `T`  | `U`  | `V`  | `W`  | `X`  | `Y`  | `Z`  | `SPACE` | `NEWLINE` | `TAB` |
| --------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | --- | --- | --- |
| Value    | `0`    | `1` | `2` | `3` | `4` | `5` | `6` | `7` | `8` | `9` | `10` | `11` | `12` | `13` | `14` | `15` | `16` | `17` | `18` | `19` | `20` | `21` | `22` | `23` | `24` | `25` | `26` | `27` | `28` | `29` |

##### ASCII Characters

##### Unicode Characters

### Null

### Arrays

### Objects

### Enums

## Data decoding

## References

[^1]: Numbers as of 2023, according to a report by [*Kepios*](https://www.statista.com/statistics/617136/digital-population-worldwide/)
