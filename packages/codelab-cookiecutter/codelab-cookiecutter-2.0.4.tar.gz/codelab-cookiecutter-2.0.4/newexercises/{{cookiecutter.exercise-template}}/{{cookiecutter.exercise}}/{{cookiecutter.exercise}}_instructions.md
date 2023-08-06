# {{cookiecutter.exercise.upper()}}

Exercise description goes here.

Specific testable instructions go below, in 3-level headers under the "Instructions" header

## Instructions
{% for number in range (1, cookiecutter.number_of_instructions | int +1) %}
### {{number}}
Instruction text

:::tests
{% if cookiecutter.tests_type == 'input' -%}
{%- if cookiecutter.lang in ['hs'] -%}
{{cookiecutter.exercise.capitalize()}}{{cookiecutter.separator}}test{{number}}.txt
{%- elif cookiecutter.lang == 'java' -%}
tests/{{cookiecutter.exercise.capitalize()}}{{cookiecutter.separator}}test{{number}}.txt
{% else %}{{cookiecutter.exercise}}{{cookiecutter.separator}}test{{number}}.txt{% endif %}
{%- elif cookiecutter.tests_type == 'unit'-%} 
{% if cookiecutter.lang == 'py' -%}
{{cookiecutter.exercise}}_test{{number}}.py
{%- elif cookiecutter.lang == 'hs' -%}
{{cookiecutter.exercise.capitalize()}}_test{{number}}Spec.hs
{%- elif cookiecutter.lang == 'java' -%}
tests/{{cookiecutter.exercise.capitalize()}}_test{{number}}.java
{%- elif cookiecutter.lang == 'go' -%}
{{cookiecutter.exercise}}_{{number}}_test.go
{%- elif cookiecutter.lang == 'e' -%}
{{cookiecutter.exercise}}_test{{number}}.e
{%- elif cookiecutter.lang == 'c' -%}
{{cookiecutter.exercise}}.test{{number}}.c
{%- elif cookiecutter.lang in ['js','html'] -%} 
{{cookiecutter.exercise}}-test{{number}}.spec.js
{%- elif cookiecutter.lang in ['cpp'] -%} 
{{cookiecutter.exercise}}.test{{number}}.cpp{% endif %}{% endif %}
:::

:::hint
Optional hint
:::
{% endfor %}