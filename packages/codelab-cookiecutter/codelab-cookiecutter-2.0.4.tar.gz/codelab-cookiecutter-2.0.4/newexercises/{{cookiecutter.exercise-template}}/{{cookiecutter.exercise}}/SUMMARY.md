{% for task in range (1, cookiecutter.tasks_number | int +1) %}* [Practice: {{cookiecutter.exercise.capitalize()}}](exercises/{{cookiecutter.exercise}}/{{cookiecutter.exercise}}{{cookiecutter.separator}}instructions.md) {% endfor %}

