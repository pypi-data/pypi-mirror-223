# codelab-cookiecutter


Exercise generation tool based on cookiecutter project. 



### Usage

To generate exrcises

```python

% gen --help

Usage: gen [OPTIONS]

Options:
  --name                          Name of the exercise
  --n INTEGER                     Number of instructions in exercise.
  --t INTEGER                     Number of exercises.
  --lang [python3|ruby|clojure|php|nodejs|scala|go|c_plus|java|v_basic|c_sharp|bash|objective_c|mysql|perl|rust]
  --help                          Show this message and exit.


% gen name --lab1 --n 3  --t 2

top
|-- exercises
|   |-- exercise1
|   |-- exercise2
|       |--exercise_initial.py
|       |--exercises_instructions.md
|       |--exercise_solution.py.text
|       |-- exercise_tests_1.py
|       |-- exercise_tests_2.py 
|      
|-- course-config.json
`-- SUMMARY.md