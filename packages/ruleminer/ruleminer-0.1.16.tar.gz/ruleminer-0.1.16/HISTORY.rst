=======
History
=======

0.1.0 (2021-11-21)
------------------

* First release on PyPI.

0.1.1 (2021-11-23)
------------------

* Added more documentation to the README text

0.1.2 (2022-1-20)
-----------------

* Bug fixes wrt some complex expressions

0.1.3 (2022-1-26)
-----------------

* Optimized rule generation process

0.1.4 (2022-1-26)
-----------------

* Evaluated columns in then part are now dependent on if part of rule

0.1.5 (2022-1-30)
-----------------

* Rule with quantiles added (including evaluating intermediate results)

0.1.6 and 0.1.7 (2022-2-1)
--------------------------

* A number of optimization in rule generation process

0.1.8 (2022-2-3)
----------------

* Rule power factor metric added

0.1.12 (2022-5-11)
------------------

* Optimizations: metric calculations are done with boolean masks of DataFrame

0.1.14 (2023-4-17)
------------------

* Nested functions added
* substr and in operators added

0.1.16 (2023-8-3)
-----------------

* Templates now do not necessarily have to contain a regex
* Bug fix when evaluating rules that contain columns that do not exist
* Templates now can start with 'if () then'
