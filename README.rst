===============================
Doyle
===============================

.. image:: https://img.shields.io/pypi/v/doyle.svg
        :target: https://pypi.python.org/pypi/doyle

.. image:: https://img.shields.io/travis/magarcia/doyle.svg
        :target: https://travis-ci.org/magarcia/doyle

.. image:: https://readthedocs.org/projects/doyle/badge/?version=latest
        :target: https://readthedocs.org/projects/doyle/?badge=latest
        :alt: Documentation Status


doyle is a tool for creating and tracking internal notes in code (inspired by
`watson <https://github.com/nhmood/watson-ruby>`_)

* Free software: `ISC license <https://github.com/magarcia/doyle/blob/master/LICENSE>`_
* Documentation: https://doyle.readthedocs.org.

Motivation
----------
This project born for find a fastest solution for watson to deal with large
projects. First benchmarks shows that :code:`doyle` is :code:`x10` faster than
:code:`watson` with large projects.

Install
-------
doyle require `The Silver Searcher <https://github.com/ggreer/the_silver_searcher>`_
to work.

doyle requires Python3. Python2 support in progress.

.. code-block::

   pip3 install git+git://github.com/myuser/foo.git@master

Features
--------
* It is an order of magnitude faster than ack.
* It ignores file patterns from your .gitignore and .hgignore.

Supported languages
-------------------

* Actionscript
* Ada
* Asm
* Cc
* Clojure
* Coffee
* Cpp
* Csharp
* Css
* Delphi
* Elisp
* Elixir
* Erlang
* Fortran
* Fsharp
* Gettext
* Go
* Groovy
* Haml
* Haskell
* Hh
* Html
* Jade
* Java
* Js
* Jsp
* Less
* Liquid
* Lisp
* Lua
* M4
* Make
* Mako
* Markdown
* Mason
* Matlab
* Nim
* Objc
* Objcpp
* Ocaml
* Perl
* Php
* Pike
* Puppet
* Python
* R
* Ruby
* Rust
* Sass
* Scala
* Scheme
* Shell
* Smalltalk
* Sql
* Stylus
* Swift
* Tcl
* Tex
* Vala
* Vb
* Vim
* Xml
* Yaml


Command line arguments
----------------------
.. code-block::

   Usage: doyle [OPTIONS] [PATHS]...

   Options:
     -q, --quiet                     Runs without displaying a user interface.
     --list-file-types               List of supported file types.
     -f, --format [plain|json|yaml]  Set output format.
     -t, --type TEXT                 Select filetypes to search for (see --list-
                                     file-types).
     -i, --ignore TEXT               Ignore files/directories matching PATTERN.
     -c, --count                     Only print the number of matches for each
                                     type.
     --version                       Show the version and exit.
     --help                          Show this message and exit.

.doylerc
--------
doyle supports an RC file that allows for reusing common settings without
repeating command line arguments every time.

The :code:`.doylerc` is placed in every directory that doyle is run from as
opposed to a unified file (in :code:`~/.doylerc` for example). The thought
process behind this is that each project may have a different set of folders to
ignore, directories to search through, and tags to look for.

For example, a C/C++ project might want to look in src/ and ignore obj/ whereas
a Node project might want to look in lib/ and ignore node_modules/.

The :code:`.doylerc` file is fairly straightforward...

**[dirs]** - This is a newline separated list of directories to look in while
parsing.

**[tags]** - This is a newline separated list of tags to look for while parsing.

**[types]** - This is a newline separated list of file types to look for while
parsing (see option :code:`--list-file-types`).

**[ignore]** - This is a newline separated list of files / folders to ignore
while parsing.

TODO
----
* Support for Python2
* Add testsuite
* Suppor for custom tag_format
* :code:`unite` output format
* Support for `GitHub <https://github.com/>`_
* Support for `Bitbucket <https://bitbucket.org/>`_
* Support for `Asana <https://asana.com/>`_
* Support for `GitLab <https://about.gitlab.com/>`_
* Support for `Jira <https://www.atlassian.com/software/jira>`_

Credits
---------

This package was created with Cookiecutter_ and the
`audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
