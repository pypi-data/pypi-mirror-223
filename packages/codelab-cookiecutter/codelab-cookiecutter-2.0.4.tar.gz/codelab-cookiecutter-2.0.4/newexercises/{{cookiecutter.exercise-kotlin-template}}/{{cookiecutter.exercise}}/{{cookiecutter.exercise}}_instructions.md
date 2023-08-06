# {{cookiecutter.exercise.upper()}}

Exercise description goes here.

Specific testable instructions go below, in 3-level headers under the "Instructions" header

## Instructions
{% for number in range (1, cookiecutter.number_of_instructions | int +1) %}
### {{number}}
Instruction text

:::tests
{% if cookiecutter.tests_type == 'input' -%}
{{cookiecutter.exercise}}{{cookiecutter.separator}}test{{number}}.txt
{%- elif cookiecutter.tests_type == 'unit'-%}
AppTest{{number}}.kt
{% endif %}
:::

:::hint
Optional hint
:::
{% endfor %}