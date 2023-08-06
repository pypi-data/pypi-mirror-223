from hexchecker import hexchecker, hexcheckerLower, hexcheckerUpper

def test_hexchecker_valid_lowercase_chars():
    assert hexchecker("abcdef") == True

def test_hexchecker_valid_uppercase_chars():
    assert hexchecker("ABCDEF") == True

def test_hexchecker_valid_mixed_chars():
    assert hexchecker("aBcDeF") == True

def test_hexchecker_valid_numbers():
    assert hexchecker("1234567890") == True

def test_hexchecker_mixed_numbers_and_chars():
    assert hexchecker("1234567890aBcDeF") == True

def test_hexchecker_invalid_chars():
    assert hexchecker("abcdefg") == False

def test_hexchecker_invalid_mixed_numbers_and_chars():
    assert hexchecker("97863hgfe347") == False

##

def test_hexcheckerLower_valid_lowercase_chars():
    assert hexcheckerLower("abcdef") == True

def test_hexcheckerLower_valid_uppercase_chars():
    assert hexcheckerLower("ABCDEF") == False

def test_hexcheckerLower_valid_mixed_chars():
    assert hexcheckerLower("aBcDeF") == False

def test_hexcheckerLower_valid_numbers():
    assert hexcheckerLower("1234567890") == True

def test_hexcheckerLower_mixed_numbers_and_chars():
    assert hexcheckerLower("1234567890aBcDeF") == False

def test_hexcheckerLower_invalid_chars():
    assert hexchecker("abcdefg") == False

def test_hexcheckerLower_invalid_mixed_numbers_and_chars():
    assert hexcheckerLower("97863hgfe347") == False
    
##

def test_hexcheckerUpper_valid_lowercase_chars():
    assert hexcheckerUpper("abcdef") == False

def test_hexcheckerUpper_valid_uppercase_chars():
    assert hexcheckerUpper("ABCDEF") == True

def test_hexcheckerUpper_valid_mixed_chars():
    assert hexcheckerUpper("aBcDeF") == False

def test_hexcheckerUpper_valid_numbers():
    assert hexcheckerUpper("1234567890") == True

def test_hexcheckerUpper_mixed_numbers_and_chars():
    assert hexcheckerUpper("1234567890aBcDeF") == False

def test_hexcheckerUpper_invalid_chars():
    assert hexcheckerUpper("abcdefg") == False

def test_hexcheckerUpper_invalid_mixed_numbers_and_chars():
    assert hexcheckerUpper("97863hgfe347") == False