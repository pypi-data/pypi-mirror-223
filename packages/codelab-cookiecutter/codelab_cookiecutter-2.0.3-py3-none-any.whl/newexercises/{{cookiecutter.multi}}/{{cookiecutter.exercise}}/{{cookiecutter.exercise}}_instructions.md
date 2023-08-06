# {{cookiecutter.exercise.upper()}}

Exercise description goes here.

Specific testable instructions go below, in 3-level headers under the "Instructions" header

## Instructions
{% for number in range (1, cookiecutter.number_of_instructions | int +1) %}
### {{number}}
Instruction text

:::tests
{{cookiecutter.exercise}}{{cookiecutter.separator}}test{{number}}.txt
:::

:::hint
Optional hint
:::
{% endfor %}