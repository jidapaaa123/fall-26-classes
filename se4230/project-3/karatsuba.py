# =============WARM-UP=============
## Search for "Warm-up (easy): get comfortable with the representation"

# =============CHECKPOINT=============
## Search for "Checkpoint (medium): the naive divide-and-conquer split"

# =============MAIN=============
## Search for "Main: Karatsuba"

# ----Starter Code-----

# Provided digit-string arithmetic and tests (click to expand)
base = 10

def full_add(x: str, y: str, carry_in: str='0'):
    """Returns (carry_out, sum_digit) as strings from adding two digit strings"""
    return full_add.lookup[x,y,carry_in]
full_add.lookup = {(str(x),str(y),str(c)): (str((x + y + c) // base), str((x + y + c) % base)) for x in range(base) for y in range(base) for c in range(base)}

def single_digit_multiply(x, y):
    """Returns (high_digit, low_digit) as strings from multiplying two digit strings"""
    return single_digit_multiply.lookup[x,y]
single_digit_multiply.lookup = {(str(x),str(y)): (str((x * y) // base), str((x * y) % base)) for x in range(base) for y in range(base)}

def single_digit_complement(digit):
    """Returns 9's complement of digit string"""
    return single_digit_complement.lookup[digit]
single_digit_complement.lookup = {str(digit): (str(9-digit)) for digit in range(base)}

def get_digit_at(x: str, i: int):
    """Returns digit string at position i from right (0-indexed) in number string x"""
    return x[-1 - i] if i < len(x) else '0'

def sign_extend(x: str, n: int):
    """Returns number string x extended to n digits by repeating its first digit"""
    sign_digit = x[0]
    return sign_digit * (n - len(x)) + x

def remove_leading_zeros(x: str):
    """Returns number string x with leading zeros stripped, preserving '0' for zero"""
    stripped = x.lstrip('0')
    return stripped if stripped != '' else '0'

def n_digit_add(x, y):
    """Returns sum as string of number strings x and y with modular arithmetic (wraps at n digits)"""
    carry = '0'
    result = []
    n = max(len(x), len(y))
    for i in range(n):
        carry, sum_digit = full_add(get_digit_at(x, i), get_digit_at(y, i), carry)
        result.append(sum_digit)
    result.append(carry)
    return remove_leading_zeros(''.join(reversed(result)))

def tens_complement(x):
    """Returns 10's complement as string: (10^n - x) for n-digit number string x"""
    n = len(x)
    complement = ''.join(str(9 - int(d)) for d in x)
    result = n_digit_add(complement, '1'.zfill(n))
    return result.zfill(n)

def n_digit_subtract(x, y):
    """Returns difference as string (x - y) using 10's complement addition on number strings"""
    n = max(len(x), len(y))
    x = x.zfill(n)
    y = y.zfill(n)
    y_complement = tens_complement(y)
    result = n_digit_add(x, y_complement)
    # If result length > n, we had a carry out (positive result)
    # If result length == n, check if we wrapped around (negative result)
    if len(result) > n:
        return remove_leading_zeros(result[1:])  # Drop the carry-out for positive results
    else:
        return remove_leading_zeros(result)

def left_shift(x: str, k: int):
    """Returns number string x * base^k (shift left k positions)"""
    return remove_leading_zeros(x + '0' * k)

def build_number_from_digits(a: list[str]):
    """Returns number string from digit string list [ones, tens, hundreds, ...]"""
    return remove_leading_zeros(''.join(reversed(a)))

def grade_school_multiply(x: str, y: str):
    """Returns product as string of number strings x and y using grade-school algorithm - O(n^2)"""
    result = '0'
    for i in range(len(y)):
        carry = '0'
        partial_product = []
        for j in range(len(x)):
            hi, lo = single_digit_multiply(get_digit_at(y, i), get_digit_at(x, j))
            carry_from_add, sum_digit = full_add(lo, carry)
            partial_product.append(sum_digit)
            carry = n_digit_add(hi, carry_from_add)
        if carry != '0':
            partial_product.append(carry)
        result = n_digit_add(result, left_shift(build_number_from_digits(partial_product), i))
    return remove_leading_zeros(result)

# Checkpoint (medium): the naive divide-and-conquer split
def divide_and_conquer_multiply(x, y):
    # Padding
    n = max(len(x), len(y))
    x, y = x.zfill(n), y.zfill(n)
    
    # Base case
    if n == 1:
        (hi, lo) = single_digit_multiply(x, y)
        return remove_leading_zeros(hi + lo)
    
    # CEILING, not floor: ex: n = 5 shall yield m = 3
    m = (n + 1) // 2
    
    x_hi, x_lo = x[: n - m], x[n - m:]
    y_hi, y_lo = y[: n - m], y[n - m:]
    
    xHi_yHi = divide_and_conquer_multiply(x_hi, y_hi)
    xHi_yLo = divide_and_conquer_multiply(x_hi, y_lo)
    xLo_yHi = divide_and_conquer_multiply(x_lo, y_hi)
    xLo_yLo = divide_and_conquer_multiply(x_lo, y_lo)
    
    unshifted_middle_term = n_digit_add(xHi_yLo, xLo_yHi)
    
    # it's fine for * here cuz it's for shifting and shifting is cheap?
    first_term = left_shift(xHi_yHi, 2*m)
    middle_term = left_shift(unshifted_middle_term, m)
    sum = n_digit_add(first_term, middle_term)
    sum = n_digit_add(sum, xLo_yLo)
    return remove_leading_zeros(sum)

# Main: Karatsuba
def karatsuba(x, y):
    # Padding
    n = max(len(x), len(y))
    x, y = x.zfill(n), y.zfill(n)
    
    # Base case
    if n == 1:
        (hi, lo) = single_digit_multiply(x, y)
        return remove_leading_zeros(hi + lo)
    
    # CEILING, not floor: ex: n = 5 shall yield m = 3
    m = (n + 1) // 2
    
    x_hi, x_lo = x[: n - m], x[n - m:]
    y_hi, y_lo = y[: n - m], y[n - m:]
    
    xHi_yHi = karatsuba(x_hi, y_hi)
    xLo_yLo = karatsuba(x_lo, y_lo)
    p3 = karatsuba(n_digit_add(x_hi, x_lo), n_digit_add(y_hi, y_lo))
    
    unshifted_middle_term = n_digit_subtract(p3, xHi_yHi)
    unshifted_middle_term = n_digit_subtract(unshifted_middle_term, xLo_yLo)  
    
    # it's fine for * here cuz it's for shifting and shifting is cheap?
    first_term = left_shift(xHi_yHi, 2*m)
    middle_term = left_shift(unshifted_middle_term, m)
    sum = n_digit_add(first_term, middle_term)
    sum = n_digit_add(sum, xLo_yLo)
    return remove_leading_zeros(sum)

# Provided tests for the given functions -- 
# copy these in as-is (click to expand)
import pytest

@pytest.mark.parametrize("x,y,carry_out,sum_digit", [
    ('0','0','0','0'),
    ('0','1','0','1'),
    ('1','0','0','1'),
    ('1','1','0','2'),
    ('0','9','0','9'),
    ('9','0','0','9'),
    ('1','9','1','0'),
    ('9','1','1','0'),
    ('9','8','1','7'),
    ('7','8','1','5'),
    ('9','9','1','8'),
])
def test_full_add(x, y, carry_out, sum_digit):
    assert (carry_out, sum_digit) == full_add(x, y)

@pytest.mark.parametrize("x,y,hi,lo", [
    ('0','0','0','0'),
    ('0','1','0','0'),
    ('1','0','0','0'),
    ('1','1','0','1'),
    ('0','9','0','0'),
    ('9','0','0','0'),
    ('1','9','0','9'),
    ('9','1','0','9'),
    ('9','8','7','2'),
    ('7','8','5','6'),
    ('9','9','8','1'),
])
def test_single_digit_multiply(x, y, hi, lo):
    assert (hi, lo) == single_digit_multiply(x, y)

@pytest.mark.parametrize("x,i,digit", [
    ('012345', 0, '5'),
    ('012345', 1, '4'),
    ('012345', 2, '3'),
    ('012345', 3, '2'),
    ('012345', 4, '1'),
    ('012345', 5, '0'),
])
def test_get_digit_at(x, i, digit):
    assert digit == get_digit_at(x, i)

@pytest.mark.parametrize("x,n,expected", [
    ('0123', 5, '00123'),
    ('123', 3, '123'),
    ('0005', 4, '0005'),
    ('999', 6, '999999'),
    ('0', 3, '000'),
    ('1', 4, '1111'),
])
def test_sign_extend(x, n, expected):
    assert expected == sign_extend(x, n)

@pytest.mark.parametrize("x,expected", [
    ('00123', '123'),
    ('123', '123'),
    ('0', '0'),
    ('000', '0'),
    ('00000123', '123'),
    ('100', '100'),
])
def test_remove_leading_zeros(x, expected):
    assert expected == remove_leading_zeros(x)

@pytest.mark.parametrize("x,y,expected", [
    ('0', '0', '0'),
    ('1', '1', '2'),
    ('5', '7', '12'),
    ('99', '1', '100'),
    ('123', '456', '579'),
    ('999', '1', '1000'),
    ('8888', '1111', '9999'),
])
def test_n_digit_add(x, y, expected):
    assert expected == n_digit_add(x, y)

@pytest.mark.parametrize("x,expected", [
    ('1', '9'),
    ('01', '99'),
    ('5', '5'),
    ('123', '877'),
    ('999', '001'),
    ('0001', '9999'),
])
def test_tens_complement(x, expected):
    assert expected == tens_complement(x)

@pytest.mark.parametrize("x,y,expected", [
    ('5', '3', '2'),
    ('10', '5', '5'),
    ('100', '1', '99'),
    ('50', '25', '25'),
])
def test_n_digit_subtract(x, y, expected):
    assert expected == n_digit_subtract(x, y)

@pytest.mark.parametrize("x,k,expected", [
    ('1', 0, '1'),
    ('1', 1, '10'),
    ('5', 2, '500'),
    ('123', 3, '123000'),
    ('0', 5, '0'),
    ('99', 2, '9900'),
])
def test_left_shift(x, k, expected):
    assert expected == left_shift(x, k)

@pytest.mark.parametrize("digits,expected", [
    (['5', '4', '3', '2', '1'], '12345'),
    (['0'], '0'),
    (['1', '2', '3'], '321'),
    (['0', '0', '0', '1'], '1000'),
    (['5'], '5'),
])
def test_build_number_from_digits(digits, expected):
    assert expected == build_number_from_digits(digits)

@pytest.mark.parametrize("x,y,expected", [
    ('0', '0', '0'),
    ('1', '1', '1'),
    ('5', '7', '35'),
    ('9', '9', '81'),
    ('1000', '1000', '1000000'),
    ('2', '3', '6'),
    ('10', '10', '100'),
    ('12345', '34567', '426729615'),
    # Warm-up (easy): get comfortable with the representation
    # ('-1', '2', '-2'), pls don't run this one
    ('100', '23', '2300'),
    ('34', '512', '17408'),
    ('123', '456', '56088')
])
def test_grade_school_multiply(x, y, expected):
    assert expected == grade_school_multiply(x, y)

@pytest.mark.parametrize("x,y,expected", [
    ('0', '0', '0'),
    ('1', '1', '1'),
    ('5', '7', '35'),
    ('9', '9', '81'),
    ('1000', '1000', '1000000'),
    ('2', '3', '6'),
    ('10', '10', '100'),
    ('12345', '34567', '426729615'),
    ('100', '23', '2300'),
    ('34', '512', '17408'),
    ('123', '456', '56088')
])    
def test_divide_and_conquer_multiply(x, y, expected):
    assert expected == divide_and_conquer_multiply(x, y)
    
@pytest.mark.parametrize("x,y,expected", [
    ('0', '0', '0'),
    ('1', '1', '1'),
    ('5', '7', '35'),
    ('9', '9', '81'),
    ('1000', '1000', '1000000'),
    ('2', '3', '6'),
    ('10', '10', '100'),
    ('12345', '34567', '426729615'),
    ('100', '23', '2300'),
    ('34', '512', '17408'),
    ('123', '456', '56088')
])    
def test_karatsuba(x, y, expected):
    assert expected == karatsuba(x, y)
    