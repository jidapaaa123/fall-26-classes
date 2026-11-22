import pytest
import random
import itertools

from pulp import LpProblem, LpMaximize, value, HiGHS
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


# Part 2: hard-coded ILP encodings
 
# Satisfiable: (a or b) and (not a or c) and (not b or not c)
F_SMALL_SAT = And([
    Or([Lit('a'), Lit('b')]),
    Or([Not('a'), Lit('c')]),
    Or([Not('b'), Not('c')]),
])
 
# Unsatisfiable: (x) and (not x)
F_SMALL_UNSAT = And([
    Or([Lit('x')]),
    Or([Not('x')]),
])
 
def solve_hardcoded_sat():
    """For f = (a or b) and (not a or c) and (not b or not c)"""
    prob = LpProblem("hardcoded_sat", LpMaximize)
 
    # Input variables
    a = prob.add_variable("a", cat="Binary")
    b = prob.add_variable("b", cat="Binary")
    c = prob.add_variable("c", cat="Binary")
 
    # NOT gadgets: not_a, not_b, not_c
    not_a = prob.add_variable("not_a", cat="Binary")
    not_b = prob.add_variable("not_b", cat="Binary")
    not_c = prob.add_variable("not_c", cat="Binary")
 
    # Clause outputs (each clause is an OR gate)
    c1 = prob.add_variable("c1", cat="Binary")  # a or b
    c2 = prob.add_variable("c2", cat="Binary")  # not a or c
    c3 = prob.add_variable("c3", cat="Binary")  # not b or not c
 
    # AND gates chaining the clauses: and12 = c1 and c2, out = and12 and c3
    and12 = prob.add_variable("and12", cat="Binary")
    out = prob.add_variable("out", cat="Binary")
 
    # NOT gadgets
    prob += not_a == 1 - a
    prob += not_b == 1 - b
    prob += not_c == 1 - c
 
    # c1 = a OR b
    prob += c1 >= a
    prob += c1 >= b
    prob += c1 <= a + b
 
    # c2 = not_a OR c
    prob += c2 >= not_a
    prob += c2 >= c
    prob += c2 <= not_a + c
 
    # c3 = not_b OR not_c
    prob += c3 >= not_b
    prob += c3 >= not_c
    prob += c3 <= not_b + not_c
 
    # and12 = c1 AND c2
    prob += and12 <= c1
    prob += and12 <= c2
    prob += and12 >= c1 + c2 - 1
 
    # out = and12 AND c3
    prob += out <= and12
    prob += out <= c3
    prob += out >= and12 + c3 - 1
 
    # Objective: the whole formula must be True == 1.
    prob += out == 1
 
    stats = prob.solve(HiGHS(msg=False))
    if stats.status_str != "Optimal": # Not found
        return None
    return {
        "a": round(value(a)) == 1,
        "b": round(value(b)) == 1,
        "c": round(value(c)) == 1,
    }
 
 
def solve_hardcoded_unsat():
    prob = LpProblem("hardcoded_unsat", LpMaximize)
 
    x = prob.add_variable("x", cat="Binary")
    not_x = prob.add_variable("not_x", cat="Binary")
    out = prob.add_variable("out", cat="Binary")  # out = x AND not_x
 
    # NOT gadget
    prob += not_x == 1 - x
 
    # out = x AND not_x 
    prob += out <= x
    prob += out <= not_x
    prob += out >= x + not_x - 1
 
    prob += out == 1
 
    stats = prob.solve(HiGHS(msg=False))
    if stats.status_str != "Optimal":
        return None
    return {"x": round(value(x)) == 1}
 
# Part 2 tests
def test_hardcoded_sat_finds_satisfying_assignment():
    assignment = solve_hardcoded_sat()
    assert assignment is not None
    assert verify_sat(F_SMALL_SAT, assignment)
 
def test_hardcoded_unsat_is_infeasible():
    assert solve_hardcoded_unsat() is None
 
def test_unsat_formula_really_is_unsat_by_brute_force():
    # Sanity check, no pulp
    assert not verify_sat(F_SMALL_UNSAT, {'x': True})
    assert not verify_sat(F_SMALL_UNSAT, {'x': False})


# Part 3: sat(f) via general reduction to ILP

def _not_gate(prob, a, name):
    """Return a new binary variable constrained to equal NOT a."""
    n = prob.add_variable(name, cat="Binary")
    prob += n == 1 - a
    return n
 
 
def _or_gate(prob, a, b, name):
    """Return a new binary variable constrained to equal a OR b."""
    o = prob.add_variable(name, cat="Binary")
    prob += o >= a
    prob += o >= b
    prob += o <= a + b
    return o
 
 
def _and_gate(prob, a, b, name):
    """Return a new binary variable constrained to equal a AND b."""
    x = prob.add_variable(name, cat="Binary")
    prob += x <= a
    prob += x <= b
    prob += x >= a + b - 1
    return x
 
 
def _chain(prob, items, gate, prefix, counter):
    """Fold a non-empty list of ILP variables with a binary gate, left to right."""
    result = items[0]
    for item in items[1:]:
        result = gate(prob, result, item, f"{prefix}{next(counter)}")
    return result
 
 
def sat(formula: And):
    if not formula.terms:
        return {}
 
    names = list(dict.fromkeys(
        lit.var for clause in formula.terms for lit in clause.literals
    ))
 
    prob = LpProblem("sat_reduction", LpMaximize)
    counter = itertools.count()  
 
    # Input variables.
    inputs = {name: prob.add_variable(f"x{i}", cat="Binary")
              for i, name in enumerate(names)}
 
    negations = {}
 
    def literal_var(lit):
        if lit.is_true:
            return inputs[lit.var]
        if lit.var not in negations:
            negations[lit.var] = _not_gate(
                prob, inputs[lit.var], f"not_x{names.index(lit.var)}")
        return negations[lit.var]
 
    # One output variable per clause.
    clause_outputs = []
    for k, clause in enumerate(formula.terms):
        if not clause.literals:
            empty = prob.add_variable(f"empty{k}", cat="Binary")
            prob += empty == 0
            clause_outputs.append(empty)
        else:
            lits = [literal_var(lit) for lit in clause.literals]
            clause_outputs.append(_chain(prob, lits, _or_gate, "or", counter))
 
    out = _chain(prob, clause_outputs, _and_gate, "and", counter)
 
    prob += out
    prob += out == 1
 
    stats = prob.solve(HiGHS(msg=False))
    if stats.status_str != "Optimal":
        return None
    return {name: round(value(var)) == 1 for name, var in inputs.items()}
 
 
# Part 3 tests

def test_sat_handout_formula():
    assignment = sat(f)
    assert assignment is not None
    assert verify_sat(f, assignment)
 
def test_sat_small_satisfiable():
    assignment = sat(F_SMALL_SAT)
    assert assignment is not None
    assert verify_sat(F_SMALL_SAT, assignment)
 
def test_sat_small_unsatisfiable():
    assert sat(F_SMALL_UNSAT) is None

if __name__ == "__main__":
    print ("Run pytest on file")
    
