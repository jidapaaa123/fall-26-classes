# PART 1: check .pdf  
# PART 2: check .pdf  
# PART 3.1: check .pdf
# PART 3.2: check huffman.py

# OPTIONAL PROVIDED TESTS
"""Optional tests for Part 3 (Huffman codec).

Huffman's algorithm can break ties either way, so these never check for a particular
bit string -- only for things every correct codec agrees on: decoding undoes encoding,
code lengths when there are no ties, and the total length of an encoded message.

The three functions in this first block are the only place the tests care what you
named things; point them at your own code and the rest just works.
"""
import random

import pytest

import huffman as yours


def build(frequencies):
    """frequencies: a list of (symbol, frequency) pairs"""
    return yours.huffman_codec(frequencies)


def encode(codec, symbols):
    return list(codec.encode(symbols))


def decode(codec, bits):
    return list(codec.decode(bits))


def message(frequencies):
    """Each symbol repeated as many times as its frequency, in a shuffled order."""
    symbols = [symbol for symbol, count in frequencies for _ in range(count)]
    random.Random(0).shuffle(symbols)
    return symbols


TEXTBOOK = [("a", 45), ("b", 13), ("c", 12), ("d", 16), ("e", 9), ("f", 5)]
SKEWED = [("w", 8), ("x", 1), ("y", 2), ("z", 4)]
TIED = [("a", 1), ("b", 1), ("c", 2), ("d", 2), ("e", 4)]
WORDS = [("the", 7), ("cat", 3), ("sat", 2), ("on", 2), ("mat", 1)]


def test_encode_produces_only_bits():
    assert set(encode(build(TEXTBOOK), "abcdef")) == {0, 1}


@pytest.mark.parametrize("frequencies", [TEXTBOOK, SKEWED, TIED, WORDS])
def test_decode_undoes_encode(frequencies):
    codec = build(frequencies)
    symbols = message(frequencies)
    assert symbols == decode(codec, encode(codec, symbols))


# --- No ties, so every correct tree gives each symbol the same code length --

@pytest.mark.parametrize("frequencies,lengths", [
    (TEXTBOOK, {"a": 1, "b": 3, "c": 3, "d": 3, "e": 4, "f": 4}),
    (SKEWED, {"w": 1, "z": 2, "y": 3, "x": 3}),
    ([("yes", 9), ("no", 1)], {"yes": 1, "no": 1}),
])
def test_code_lengths(frequencies, lengths):
    codec = build(frequencies)
    assert lengths == {symbol: len(encode(codec, [symbol])) for symbol in lengths}


# --- Ties can change the tree, but never the total cost -----------------------

@pytest.mark.parametrize("frequencies,cost", [
    (TEXTBOOK, 224),
    (SKEWED, 25),
    (TIED, 22),
    (WORDS, 31),
])
def test_encoded_message_has_optimal_length(frequencies, cost):
    assert cost == len(encode(build(frequencies), message(frequencies)))


def test_equal_frequencies_give_equal_code_lengths():
    codec = build([(symbol, 1) for symbol in "abcdefgh"])
    assert {3} == {len(encode(codec, [symbol])) for symbol in "abcdefgh"}


# --- Any iterable works, not just lists ----------------------------------------

def test_encode_and_decode_take_any_iterable():
    codec = build(TEXTBOOK)
    bits = encode(codec, "faced")
    assert list("faced") == decode(codec, iter(bits))
    assert bits == encode(codec, (letter for letter in "faced"))


# --- Big inputs: each should finish in about a second -------------------------
# If one takes much longer, look for a hidden O(n) step inside a loop
# (list slicing, string concatenation, a linear search for the lightest node...).

def test_many_symbols():
    frequencies = [(symbol, 1) for symbol in range(2 ** 12)]
    codec = build(frequencies)
    assert {12} == {len(encode(codec, [symbol])) for symbol, _ in frequencies}


def test_long_message():
    codec = build(TEXTBOOK)
    symbols = message(TEXTBOOK) * 2000
    bits = encode(codec, symbols)
    assert 224 * 2000 == len(bits)
    assert symbols == decode(codec, bits)