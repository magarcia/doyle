# -*- coding: utf-8 -*-

# [TODO] - Support for Python2
# [TODO] - Add testsuite
# [TODO] - Support for GitHub
# [TODO] - Support for Bitbucket
# [TODO] - Support for Asana
# [TODO] - Support for GitLab
# [TODO] - Support for Jira

import pkg_resources  # part of setuptools
import click
from os import getcwd, path
from re import search, IGNORECASE
from subprocess import Popen, PIPE
from configparser import ConfigParser

from doyle.definitions import COMMENT_DEFINITIONS
VERSION = pkg_resources.require("doyle")[0].version
APP_NAME = pkg_resources.require("doyle")[0].project_name


# [TODO] - Suppor for custom tag_format
def read_config():
    parser = ConfigParser(allow_no_value=True)
    cfg = path.join(getcwd(), '.doylerc')
    parser.read(cfg)
    rv = {}
    for section in parser.sections():
        for key, value in parser.items(section):
            if section not in rv.keys():
                rv[section] = []
            rv[section].append(key)
    return rv


def rchop(string, ending):
    if string.endswith(ending):
        return string[:-len(ending)]
    return string


def process_output(types, input, path, endings=[]):
    """
    """
    regexp = "(%s)\W+\s*\W\s*(.+)" % '|'.join(types)
    current_file = None
    outs = {}
    matches = {}
    for line in input:
        if len(line) == 0:
            continue

        if line.startswith(':'):
            if current_file is not None:
                if len(outs):
                    matches[current_file.replace('%s/' % path, '')] = outs
            current_file = line.split(':')[1]
            outs = {}

        elif line[0].isdigit():
            comment = line.split(':', 1)
            if len(comment) == 2:
                line_number = comment[0].split(';')[0]
                comment = comment[1].strip()
                m = search(regexp, comment, IGNORECASE)
                if m:
                    type = m.group(1).lower()
                    comment = m.group(2)
                    if type not in outs:
                        outs[type] = {}
                    for end in endings:
                        comment = rchop(comment, end)
                    outs[type][int(line_number)] = comment

    if current_file is not None:
        if len(outs):
            matches[current_file.replace('%s/' % path, '')] = outs

    return matches


def find_comments(types, ext, c, endings, ignore, path):
    regex = "\"^\\s*(%s)\W+?(%s).+$\"" % ('|'.join(c), '|'.join(types))

    command = 'ag --ackmate --ignore-case %s --%s  %s %s' % (ignore, ext,
                                                             regex, path)

    p = Popen([command], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    output, err = p.communicate()
    return process_output(types, output.decode('utf-8').split('\n'), path,
                          endings)


def print_file_types(ctx, param, value, *args, **kwargs):
    if not value or ctx.resilient_parsing:
        return

    for k in sorted(COMMENT_DEFINITIONS.keys()):
        click.echo("* %s" % k.capitalize())
    ctx.exit()


# [TODO] - unite output format
def print_formated(fmatches, format):
    if format == 'json':
        from json import dumps
        click.echo(dumps(fmatches,
                         sort_keys=True,
                         indent=2,
                         separators=(',', ': ')))
    elif format == 'yaml':
        from yaml import dump
        click.echo(dump(fmatches,
                        default_flow_style=False,
                        width=80,
                        indent=4))
    else:
        to_print = []
        for filename, comments in sorted(fmatches.items()):
            to_print.append(click.style(filename, fg='red', bold=True))
            for type, lines in sorted(comments.items()):
                to_print.append(click.style(type, fg='blue', bold=True))
                for number, content in sorted(lines.items()):
                    to_print.append(' '.join([
                        click.style('  line %d -' % number,
                                    fg='white'), click.style(content,
                                                             bold=True)
                    ]))
            to_print.append('\n')

        if format == 'plain':
            click.echo('\n'.join(to_print))
        else:
            click.echo_via_pager('\n'.join(to_print))


# [TODO] - Merge info from config file and options
@click.command()
@click.option('-q',
              '--quiet',
              is_flag=True,
              help='Runs without displaying a user interface.')
@click.option('--list-file-types',
              is_flag=True,
              callback=print_file_types,
              expose_value=False,
              is_eager=True,
              help='List of supported file types.')
@click.option('-f',
              '--format',
              type=click.Choice(['plain', 'json', 'yaml']),
              help='Set output format.')
@click.option('-t',
              '--type',
              multiple=True,
              help='Select filetypes to search for (see --list-file-types).')
@click.option('-i',
              '--ignore',
              multiple=True,
              help='Ignore files/directories matching PATTERN.')
@click.option('-c',
              '--count',
              is_flag=True,
              help='Only print the number of matches for each type.')
@click.version_option(version=VERSION)
@click.argument('paths', nargs=-1, type=click.Path(), required=False)
def cli(quiet, paths, format, type, count, ignore):

    # Get paths
    if len(paths) == 0:
        paths = [getcwd()]
    path = ' '.join(paths)

    # Read config
    config = read_config()

    # Get ignores
    ignore = ''
    if 'ignore' in config.keys():
        ignore = '--ignore %s' % ' --ignore '.join(config['ignore'])

    # Get tags
    tags = ['fix', 'review', 'todo' 'hack']
    if 'tags' in config.keys():
        tags = config['tags']

    # Get types
    selected = {}
    if 'types' in config.keys() and len(type) == 0:
        type = config['types']

    if len(type) > 0:
        for i in type:
            try:
                selected[i] = COMMENT_DEFINITIONS[i]
            except KeyError:
                raise click.BadParameter(
                    'should be a valid type (see --list-file-types)',
                    param_hint='type')
    else:
        selected = COMMENT_DEFINITIONS

    fmatches = {}
    for ext, comment in selected.items():
        fmatches.update(find_comments(tags, ext, comment['endings'], comment[
            'endings'], ignore, path))

    if not quiet:
        print_formated(fmatches, format)


if __name__ == '__main__':
    cli(auto_envvar_prefix=APP_NAME.upper())
