Given SMT-LIB horn clauses, attempts to format the clauses to the CHC-COMP format. Original script from @dddejan.

- splits multiple-query scripts to single query ones (separated by `exit`)
- forces predicate applications' arguments to be (distinct) variables

## Setup

To setup z3:

```
pip installl -r requirements.txt
```

To format a benchmark:

```
$ cat test/inline_test_00.smt2
(set-logic HORN)
(set-info :status sat)
(declare-fun p (Int) Bool)
(declare-fun q (Int) Bool)
(assert (forall ((x Int)) (=> (> x 0) (p x))))
(assert (forall ((x Int)) (=> (p x) (q x))))
(assert (forall ((x Int)) (=> (q x) (> x 0))))

$ python translate.py test/inline_test_00.smt2
(set-logic HORN)
(assert
  (forall ((A Int)) (=> (and (not (<= A 0))) (p A)))
)
(assert
  (forall ((A Int)) (=> (and (p A)) (q A)))
)
(assert
  (forall ((A Int)) (=> (and (q A) (<= A 0)) false))
)
(check-sat)
(exit)
```

Use `--check True` to check if a benchmark is legal:

```
$ python translate.py --check True test/multi_query.smt2
Error on file test/multi_query.smt2
illegal head: non-distinct arguments, (:var 2) is used twice in (unknown (:var 2) (:var 2))

$ python translate.py --check True test/cst_in_head.smt2
Error on file test/cst_in_head.smt2
illegal chc: expected forall, got (not (exists ((|$alpha-2:$$tmp::2| Int))
       (and (|fail$unknown:3| |$alpha-2:$$tmp::2|))))

$ python translate.py test/cst_in_head.smt2 > test.smt2 ; python2.7 translate.py --check True test.smt2
success
```