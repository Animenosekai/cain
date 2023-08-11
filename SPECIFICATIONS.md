# The `Cain` data format

> A small yet powerful data format

## Index

- [Index](#index)
- [Purpose](#purpose)
  - [Social and economical issue](#social-and-economical-issue)
  - [Environmental issue](#environmental-issue)
- [General Idea](#general-idea)
- [Data encoding](#data-encoding)
  - [Arrays](#arrays)
    - [Case 1: Without repetition in the data](#case-1-without-repetition-in-the-data)
    - [Case 2: With repetition in the data](#case-2-with-repetition-in-the-data)
  - [Binary](#binary)
  - [Booleans](#booleans)
  - [Characters](#characters)
  - [NoneType (null)](#nonetype-null)
  - [Numbers](#numbers)
    - [Floats](#floats)
    - [Complex numbers](#complex-numbers)
    - [Integers](#integers)
  - [Objects](#objects)
    - [Case 1: No repetition in the data](#case-1-no-repetition-in-the-data)
    - [Case 2: With a repetition in the data](#case-2-with-a-repetition-in-the-data)
  - [Optionals](#optionals)
  - [Ranges](#ranges)
  - [Sets](#sets)
  - [Strings](#strings)
  - [Tuples](#tuples)
  - [Type](#type)
  - [Unions](#unions)
- [References](#references)

## Purpose

In a world where the internet is being used by more than 60% of the population[^1], and with the rise of service APIs to provide users with real-time informations on the fly, data transfers became a major part of our life. Even though most people don't notice it, us developers have the responsibilty to conduct those transfers in the most efficient way possible for several reasons

### Social and economical issue

Even though our internet speeds are becoming faster and faster with technologies such as Optical Fiber and 5G, great inequalities are to be seen worldwide with a non negligible part of consumers still using slow transfer rates technologies such as 3G for availability but also economic reasons.

This brings a huge burden for some countries to develop further as the internet is expected, and already has, a central part in any economic but also public affairs.

With up to 94%[^2] of companies now using cloud services and 67%[^2] of them having their infrastructure cloud-based, having smaller data storage options may benefit on an economic perspective.

### Environmental issue

While the current environmental footprint of online activites remains arguably low, with the mulitplication of internet users and the more intense usage of the internet in our everyday life, the small environmental impacts add up and become a substantial role in the current environmental issues.

Storage with smaller formats also means a smaller need to allocate resources for databases and data retention.

## General Idea

While formats such as [`JSON`](https://www.json.org) and [`XML`](https://www.w3.org/TR/xml/) have big overheads, aiming at both human and machine readable values, most of the time, the data will only be used within a single software or two, without even being shown once to the end user. Why bother having the human readable part for those use cases ?

Moreover, most data has and should have a fixed schema, which leverages the need to repeat it in the formatted value at the end.

Finally, some data might be redundant and used mutiple times throughout the same file. References can avoid this by simply writing the data once and reference to it in the right fields. While this might be avoided with JSON using [compression algorithms](https://developer.mozilla.org/en-US/docs/Web/HTTP/Compression) (which should definitely be used), this helps reduce the uncompressed sizes, for browsers which don't support the compression algorithms yet or use cases outside of web development and size critical environments.

This format aims at bringing the smallest data formatting possible for machine-to-machine communications by avoiding any redundancy and unnecessary syntax.

## Data encoding

Here are some examples on how the built-in datatypes are encoded with Cain.

### Arrays

#### Case 1: Without repetition in the data

Example: `[1, 2, 3]`

```python
\x00\x03  \x00\x00   \x00\x01 \x00\x02 \x00\x03
~~~~~~~~  ~~~~~~~~   ~~~~~~~~~~~~~~~~~~~~~~~~~~
Array     Number     Rest of data
Length    of repeats
```

#### Case 2: With repetition in the data

Example: `["Hello", "Hi", "Hello", "Hey"]`

```python
\x00\x04   \x00\x01    \x00\x02 \x00\x00 \x00\x02 Hello\x00        Hi\x00 Hey\x00
~~~~~~~~   ~~~~~~~~   [~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~] * n   ~~~~~~~~~~~~~~
Array      Number of   Number    Index1   Index2  Repeated         Rest of data
Length     repeats     of indices                 Data
             (n)
```

### Binary

```python
\x00\x00\x00\x0b \x48\x65\x6c\x6c\x6f\x20\x77\x6f\x72\x6c\x64
~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  size of blob                   blob itself
```

### Booleans

- `\x01` — Represents `True`
- `\x00` — Represents `False`

### Characters

Characters are encoded following the UTF-8 encoding.

From: <https://en.wikipedia.org/wiki/UTF-8#Encoding>

| Chararacter length | UTF-8 octet sequence                  |
| ------------------ | ------------------------------------- |
| 1 byte character   | `0xxxxxxx`                            |
| 2 bytes character  | `110xxxxx 10xxxxxx`                   |
| 3 bytes character  | `1110xxxx 10xxxxxx 10xxxxxx`          |
| 4 bytes character  | `11110xxx 10xxxxxx 10xxxxxx 10xxxxxx` |

> **Note**  
> The `x` has the actual code point.

### NoneType (null)

Nothing is appended, because the value does not change, we only need to know that it is `None`/`null`.

### Numbers

#### Floats

Floating point numbers are encoded following [IEEE 754](https://en.wikipedia.org/wiki/IEEE_754).
They are separated into single precision (`Float`) and double precision (`Double`) numbers.

Decimals (`Decimal`) are exact representations of decimal numbers, without any approximations. They are encoded as strings.

#### Complex numbers

Complex numbers are encoded as two consecutive floats (`Complex`) or doubles (`DoubleComplex`).

#### Integers

Integers are encoded by turning them into without using any approximation, converting them from base10 to base2.

When using the base `Int` class, you can modulate the range of encodable integers using the `short`, `long`, `signed` and `unsigned` parameters.

You can also use the different fixed size classes (`Int64`, `UInt32`, etc.)
to save time on the arguments processing.

Refer to the different implementations for more information.

### Objects

> **Note**  
> Any index in the encoded data is the index of a key in the sorted list of keys.

#### Case 1: No repetition in the data

Example: `{"username": "Anise", "favorite_number": 2}`

```python
\x00\x00   \x00\x02 Anise\x00
~~~~~~~~   ~~~~~~~~~~~~~~~~~·
Number     Rest of data
of repeats
```

#### Case 2: With a repetition in the data

Example: `{"name": "Anise", "username": "Anise", "favorite_number": 2}`

```python
\x00\x01    \x00\x02 \x00\x01 \x00\x02 Anise\x00        \x00\x02
~~~~~~~~   [~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~] * n   ~~~~~~~~~~~~~~
Number of   Number    Index1   Index2  Repeated         Rest of data
repeats     of indices                 Data
(n)
```

> **Note**  
> Unlike [Arrays](#arrays) we don't need to encode the length because it is fixed.

### Optionals

`\x00` — Represents `None`
`\x01` + value encoded by Union — If the given value is not `None`,
                                  the value will be encoded using the `Union` datatype.

### Ranges

```python
\x00 \x04 \x02
 (1)  (2)  (3)
```

1. The start of the range.
2. The end of the range.
3. The step of the range.

> **Note**  
> The integers used by default are unsigned 8-bit integers (covering the -128 to 127 range).
>
> **Note**  
> You can use the same type arguments as `Int` to change this behaviour. Refer to [`Int`](#integers) for more information.

### Sets

Because the order of the elemnts is not even maintained when making the set, the different type arguments are treated as a big `Union`.

Under the hood, *Sets* are encoded the same as [Arrays](#arrays).
Refer to [`Array`](#arrays) for more information.

### Strings

Each character is encoded using [`Character`](#characters) and the string ends with a NULL character (`\x00`).
Refer to [`Character`](#characters) for more information.

### Tuples

Under the hood, *Tuples* are encoded the same as [Arrays](#arrays).
Refer to [`Array`](#arrays) for more information.

### Type

*Types* are actually just an [Object](#objects) with the following attributes:

- `index`: The index of the Datatype in `TYPES_REGISTRY`
- `name`: If changed, the name of the Datatype
- `annotations_keys`: The keys for the annotations, in the order they appear in `annotations_values`
- `annotations_values`: The values for the annotations, in the order they appear in `annotations_values`
- `arguments`: The different type arguments

Refer to [`Object`](#objects) for more information.

### Unions

- If there is only one type argument specified, this argument will be used to encode and decode the value.
- If there are multiple types possible for the value, the index of the type used is first prepended, then the value is encoded.

```python
\x01 \x00\x02
 (1)    (2)
```

1. The index of the type in the different type arguments
2. The actual encoded data

## References

[^1]: Numbers as of 2023, according to a report by [*Kepios*](https://www.statista.com/statistics/617136/digital-population-worldwide/)

[^2]: According to an article by [*Zippia*](https://www.zippia.com/advice/cloud-adoption-statistics/), written on Dec. 19, 2022, accessed on Apr. 28, 2023
