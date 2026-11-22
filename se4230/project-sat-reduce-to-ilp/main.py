import pytest
from dataclasses import dataclass

@dataclass
class Literal:
    var: str
    is_true: bool 

def Lit(variable: str) -> Literal:
    return Literal(variable, True)

def Not(variable: str) -> Literal:
    return Literal(variable, False)

@dataclass
class Or:
    literals: list[Literal]

@dataclass
class And:
    terms: list[Or]

f = And([
    Or([Lit('a'),
        Lit('b'),
        Lit('c')]),
    Or([Not('a'),
        Lit('b'),
        Not('c')]),
    Or([Not('d'),
        Not('b')]),
    Or([Not('a'),
        Lit('c')]),
    Or([Not('b'),
        Lit('a')]),
])

def verify_sat(formula: And, assignment: dict[str, bool]) -> bool:
    return all(
        any(assignment[lit.var] == lit.is_true for lit in clause.literals) # is any literal true...
        for clause in formula.terms # ... for each island
    )


# Part 1 tests

def test_verify_sat_satisfying_assignment():
    assert verify_sat(f, {'a': True, 'b': True, 'c': True, 'd': False}) is True

def test_verify_sat_single_positive_literal():
    formula = And([Or([Lit('x')])])
    assert verify_sat(formula, {'x': True}) is True
    assert verify_sat(formula, {'x': False}) is False

def test_verify_sat_single_negative_literal():
    formula = And([Or([Not('x')])])
    assert verify_sat(formula, {'x': False}) is True
    assert verify_sat(formula, {'x': True}) is False

# ---------------------------------------------------------------------------
# Part 2: hard-coded ILP encoding (checkpoint)  -- TODO
# Part 3: sat(f) general reduction + proof      -- TODO
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    print ("Running tests...")