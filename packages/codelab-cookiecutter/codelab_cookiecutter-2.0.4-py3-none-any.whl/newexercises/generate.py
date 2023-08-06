import glob
import json
import os
import pathlib
import typing
import re
from shutil import copyfile, rmtree

import click
import cookiecutter.main as ccmain
from loguru import logger
from newexercises import utils
from newexercises.enums import Language, TestsType
from pydantic import BaseModel

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

dirname = os.path.dirname(__file__)

_file = os.path.join(dirname, 'cookiecutter.json')
primary = os.path.join(dirname, '{{cookiecutter.primary}}')
exercise = os.path.join(dirname, '{{cookiecutter.exercise-template}}')
multi = os.path.join(dirname, '{{cookiecutter.multi}}')
exercise_kotlin = os.path.join(dirname, '{{cookiecutter.exercise-kotlin-template}}')
openai = os.path.join(dirname, '{{cookiecutter.exercise-template-ai}}')


class ExerciseConfig(BaseModel):
    """Shema for exercise config"""
    name: str
    n: int


def _generate_config(name, n, t, test, lang, initial, instructions, solution, tests, ai=False):
    _config = {}
    name = name.split(' ')[0].lower()
    logger.info(f'exercises  is {t} , with {n} instructions')
    n = 1 if (lang == 'eiffel' and test != 'input') else n
    config = {'project_path': './',
              'name': 'exercises',
              'tasks_number': f'{t}',
              'lang': Language.map_to_ext(lang),
              "initial": initial,
              "instructions": instructions,
              "solution": solution,
              "tests": tests,
              'other': Language.map_to_other(lang),
              'extra': Language.map_to_extra(lang),
              'root_file': Language.map_to_default_root(lang),
              'test_file': Language.map_to_test_file(lang),
              'tests_type': test,
              'default_input': False,
              'ai': ai,
              'separator': Language.map_to_separator(lang),
              'exercises': []
              }

    if t < 2:
        config['exercises'].append(ExerciseConfig(name=name, n=n).dict())
    else:
        for exercise in range(1, t + 1):
            _config['name'] = f'{name}{exercise}'
            _config['n'] = n
            config['exercises'].append(_config.copy())
    if test != 'input':
        config['default_input'] = True

    with open(os.path.join(dirname, 'config.json'), 'w') as processed_file:
        processed_file.write(json.dumps(config, indent=4))


def _generate_exercises():
    """Generate exercise."""
    exercise_config = {}

    # Copy the cookiecutter.json from central location to all templates,
    # so we won't need to update each cookiecutter.json
    # template manually.

    sub_templates = [primary, exercise, multi]
    for template in sub_templates:
        copyfile(_file, os.path.join(template, 'cookiecutter.json'))
    # Load the custom config file.
    with open(os.path.join(dirname, 'config.json'), 'r') as f_config:
        config = json.load(f_config)

    # Create the project using the primary template.
    ccmain.cookiecutter(primary,
                        no_input=True,
                        extra_context=config,
                        overwrite_if_exists=True)

    # For each exercise, create a exercise folder using the sub template.
    for task in config['exercises']:
        exercise_config['exercise'] = task['name']  # Used for cookiecutter.json
        exercise_config['lang'] = config['lang']
        exercise_config['ai'] = config['ai']
        exercise_config["initial"] = config["initial"]
        exercise_config["instructions"] = config["instructions"]
        exercise_config["solution"] = config["solution"]
        exercise_config["tests"] = config["tests"]
        exercise_config['other'] = config['other']
        exercise_config['extra'] = config['extra']
        exercise_config['root_file'] = config['root_file']
        exercise_config['test_file'] = config['test_file']
        exercise_config['tests_type'] = config['tests_type']
        exercise_config['separator'] = config['separator']
        for instruction in range(1, task['n'] + 1):
            exercise_config['tests_number'] = instruction
            exercise_config['number_of_instructions'] = instruction
            # Create the sub folder using the sub template in the correct location
            if config['ai']:
                ccmain.cookiecutter(openai,
                                    no_input=True,
                                    extra_context=exercise_config,  # Overiddes attributes in the cookicutter.json
                                    overwrite_if_exists=True,
                                    output_dir=os.path.join(config['project_path'], config['name'])
                                    )
            else:
                if config['lang'] == Language.kotlin.ext:
                    ccmain.cookiecutter(exercise_kotlin,
                                    no_input=True,
                                    extra_context=exercise_config,  # Overiddes attributes in the cookicutter.json
                                    overwrite_if_exists=True,
                                    output_dir=os.path.join(config['project_path'], config['name'])
                                    )
                elif not config['lang'] == 'unspecified':
                    ccmain.cookiecutter(exercise,
                                    no_input=True,
                                    extra_context=exercise_config,  # Overiddes attributes in the cookicutter.json
                                    overwrite_if_exists=True,
                                    output_dir=os.path.join(config['project_path'], config['name'])
                                    )
                else:
                    ccmain.cookiecutter(multi,
                                    no_input=True,
                                    extra_context=exercise_config,
                                    overwrite_if_exists=True,
                                    output_dir=os.path.join(config['project_path'], config['name'])
                                    )
        [os.remove(i) for i in glob.glob(f'exercises/{task["name"]}/input.txt', recursive=True) if
         config['default_input']]


def _pre_check(name: str):
    exercises = [i for i in glob.glob(f'exercises/{name}/', recursive=True)]
    if len(exercises) > 0:
        logger.warning(f'exercises or exercise with name {name} already presented.')
        return False
    return True


def _reformat_exercises(name, n):
    """Rename files for html-css-js.
    exercises/lab2/lab2_initial.js --> exercises/lab2/script.js
    exercises/lab2/lab2_initial.css --> exercises/lab2/style.css
    """
    m = {'css': 'style.css',
         'html': 'index.html',
         'js': 'script.js',
         'txt': 'txt',
         'states': {'initial': '', 'solution': '.txt'}}

    if n != 1:
        [[os.rename(i, f'exercises/{i.split("/")[1]}/{m.get((i.split("/")[2]).split(".")[1])}{k}') for i in
          glob.glob(f'exercises/*/*', recursive=True) if (re.search(f'{name}[0-9]_{j}.*', i))] for j, k in
         m.get('states').items()]

    else:
        [[os.rename(i, f'exercises/{i.split("/")[1]}/{m.get((i.split("/")[2]).split(".")[1])}{k}') for i in
          glob.glob(f'exercises/*/*', recursive=True) if (re.search(f'{name}_{j}.*', i))] for j, k in
         m.get('states').items()]


def _post_gen_fixes(name, lang, t, test):
    """Apply fixes depend on language pipeline."""

    sep = utils.get_separator(lang)
    ext = Language.map_to_ext(lang)
    capitalize_name = name.capitalize()
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    if lang == 'eiffel' and test == 'input':
        [os.remove(i) for i in glob.glob(f'exercises/{name}/*.ecf', recursive=False)]
    [os.remove(i) for i in glob.glob(f'exercises/*/*.ecf', recursive=True) if lang != 'eiffel']

    if lang == 'nodejs':
        [os.rename(j, j.replace(f'_test{i + 1}', f'-test{i + 1}.spec')) for i, j in
         enumerate(sorted(glob.glob(f'exercises/*/*_test*', recursive=True), key=alphanum_key))]
    if lang == 'unspecified':
        [os.rename(j, j.replace(f'_test{i + 1}.unspecified', f'-test{i + 1}.txt')) for i, j in
         enumerate(sorted(glob.glob(f'exercises/*/*_test*', recursive=True), key=alphanum_key))]
    if lang == 'go':
        [os.rename(j, j.replace(f'_test{i + 1}', f'_{i + 1}_test')) for i, j in
         enumerate(sorted(glob.glob(f'exercises/*/*_test?.go', recursive=True), key=alphanum_key))]
    if lang == 'haskell':
        [os.rename(i, i.replace(f'{name}_initial.hs', f'{name.capitalize()}.hs')) for i in
         glob.glob(f'exercises/{name}/{name}_initial.hs', recursive=True)]
        [os.rename(i, i.replace(f'{name}_solution.hs.txt', f'{name.capitalize()}_solution.hs.txt')) for i in
         glob.glob(f'exercises/{name}/{name}_solution.hs.txt', recursive=True)]
        [os.rename(j, j.replace(f'{name}_test{i}.hs', f'{capitalize_name}_test{i}Spec.hs')) for i, j in
         enumerate(sorted(glob.glob(f'exercises/{name}/{name}_test*.*', recursive=True), key=alphanum_key), start=1)]

    if lang == 'java':
        output_dir = os.path.join('./', 'exercises')

        source_tests = os.path.join(output_dir, f'{name}/*test?.java')
        destination_tests = os.path.join(output_dir, f'{name}/tests/')

        source_initial = os.path.join(output_dir, f'{name}/*.java')
        destination_initial = os.path.join(output_dir, f'{name}/initial/')

        source_solution = os.path.join(output_dir, f'{name}/*.txt')

        destination_solution = os.path.join(output_dir, f'{name}/solution/')

        [os.remove(i) for i in glob.glob(f'exercises/*/*.n*', recursive=True)]
        [os.remove(i) for i in glob.glob(f'exercises/*/n.java', recursive=True)]
        # Capitalize names
        [os.rename(j, j.replace(f'{name}_initial.java', f'{capitalize_name}.java')) for i, j in
         enumerate(sorted(glob.glob(f'exercises/{name}/{name}_*.java', recursive=True), key=alphanum_key), start=1)]
        [os.rename(j, j.replace(f'{name}_initial.main', f'Main.java')) for i, j in
         enumerate(sorted(glob.glob(f'exercises/{name}/{name}_*.main', recursive=True), key=alphanum_key), start=1)]
        [os.rename(j, j.replace(f'{name}_solution.main.txt', f'{capitalize_name}.n')) for i, j in
         enumerate(sorted(glob.glob(f'exercises/{name}/{name}_solution.main.txt', recursive=True), key=alphanum_key),
                   start=1)]
        [os.rename(j, j.replace(f'{name}_solution.java.txt', f'{capitalize_name}_solution.java.txt')) for i, j in
         enumerate(sorted(glob.glob(f'exercises/{name}/{name}_solution.java.txt', recursive=True), key=alphanum_key),
                   start=1)]
        [os.rename(j, j.replace(f'{name}_test{i}.java', f'{capitalize_name}_test{i}.java')) for i, j in
         enumerate(sorted(glob.glob(f'exercises/{name}/{name}_*.java', recursive=True), key=alphanum_key), start=1)]

        utils.move_files(source_solution, destination_solution)
        utils.move_files(source_tests, destination_tests)
        utils.move_files(source_initial, destination_initial)

    if lang in ['cpp', 'c-lang']:
        [os.rename(i, i.replace('_test', '.test')) for i in
         glob.glob(f'exercises/{name}/{name}_test*', recursive=True)]
    if lang == 'html-css-js':
        output_dir = os.path.join('./', 'exercises')
        source = os.path.join(output_dir, f'{name}/*.txt')
        destination = os.path.join(output_dir, f'{name}/solutions/')
        [os.rename(j, j.replace(f'_test{i + 1}.html', f'-test{i + 1}.spec.js')) for i, j in
         enumerate(sorted(glob.glob(f'exercises/*/*_test*', recursive=True), key=alphanum_key))]
        _reformat_exercises(name, t)
        utils.move_files(source, destination)
    if test == TestsType.input.value:
        [os.rename(j, j.replace(f'{sep}test{i + 1}.{ext}', f'{sep}test{i + 1}.txt')) for i, j in
         enumerate(sorted(glob.glob(f'exercises/{name}/*{sep}test*.{ext}', recursive=True), key=alphanum_key))]
        [os.rename(j, j.replace(f'{sep}test{i + 1}.{ext}', f'{sep}test{i + 1}.txt')) for i, j in
         enumerate(sorted(glob.glob(f'exercises/{name}/tests/*{sep}test*.{ext}', recursive=True), key=alphanum_key))]
        [os.rename(j, j.replace(f'{sep}test{i + 1}.spec.js', f'{sep}test{i + 1}.txt')) for i, j in
         enumerate(sorted(glob.glob(f'exercises/{name}/*{sep}test*.spec.js', recursive=True), key=alphanum_key))]
        [os.rename(j, j.replace(f'test{i}Spec.hs', f'test{i}.txt')) for i, j in
         enumerate(sorted(glob.glob(f'exercises/{name}/*Spec.hs', recursive=True), key=alphanum_key), start=1)]
        [os.rename(j, j.replace(f'AppTest{i}.kt', f'{name}{sep}test{i}.txt')) for i, j in
         enumerate(sorted(glob.glob(f'exercises/{name}/*Test*.kt', recursive=True), key=alphanum_key), start=1)]

        [os.remove(i) for i in glob.glob(f'exercises/{name}/unittest_manager.e', recursive=True)]

    [os.remove(i) for i in glob.glob(f'exercises/*/*.n', recursive=True)]
    [os.remove(i) for i in glob.glob(f'exercises/*/n.{ext}', recursive=True)]
    [os.remove(i) for i in glob.glob(f'exercises/*/*.n.txt', recursive=True)]
    [os.rename(i, utils.replace_last(i, '_', sep)) for i in glob.glob(f'exercises/{name}/{name}_*')]
    [utils.fix_json(i) for i in glob.glob('exercises/*/*.json', recursive=True)]


def _remove_empty_lines(filename):
    """Overwrite the file, removing empty lines."""
    if filename:
        with open(filename) as in_file, open(filename, 'r+') as outfile:
            outfile.writelines(line for i, line in enumerate(in_file) if line.strip())
            outfile.truncate()
    else:
        with open('SUMMARY.md', 'w') as outfile:
            outfile.write("# Exercises\n")


def _merge_summaries(filenames: typing.List) -> typing.Any:
    with open('SUMMARY.md', 'a') as outfile:
        for fname in filenames:
            with open(fname, ) as infile:
                for line in infile:
                    if len(line) > 1:
                        outfile.write(line)
                    outfile.truncate()
    return 'SUMMARY.md'


def _post_gen_processing(name: str) -> None:
    """Merges summaries and moves them to the root folder."""
    _remove_empty_lines(glob.glob('SUMMARY.md')[0] if glob.glob('SUMMARY.md') else None)
    files = [f'{i}' for i in glob.glob('exercises/*/SUMMARY.md', recursive=True)]
    _merge_summaries(files)
    [os.remove(i) for i in glob.glob(f'exercises/{name}*/SUMMARY.md', recursive=True)]
    [os.remove(i) for i in glob.glob(f'exercises/log.txt', recursive=True)]
    # clear pycache
    [rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]


@click.command()
@click.option('--name', default='Reverse String', help='Name of the exercise')
@click.option('--n', default=1, help='Number of instructions in exercise.')
@click.option('--test', type=click.Choice(TestsType.values(), case_sensitive=False), prompt=False, default='unit')
@click.option('--t', default=1, help='Number of exercises.')
@click.option('--lang',
              type=click.Choice(Language.values(), case_sensitive=False), prompt=False, default='python3')
@click.option('--initial', default='xxx', help='Default code for task')
@click.option('--instructions', default='', help='Markdown instructions for task')
@click.option('--solution', default='', help='Solution code for task.')
@click.option('--tests', default='', help='Tests code for task.')
@click.option('--ai', default='True', help='If True we will use openai LLMs.')
def gen(name, n, test, t, lang, initial, instructions, solution, tests, ai=False):
    if _pre_check(name):
        _generate_config(name, n, t, test, lang, initial, instructions, solution, tests, ai)
        _generate_exercises()
        _post_gen_fixes(name, lang, t, test)
        _post_gen_processing(name)


if __name__ == '__main__':
    gen()
