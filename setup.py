from setuptools import setup
from parallelforeachsubmodule.metadata import Metadata

metadata = Metadata()


def requirements():
    """Build the requirements list for this project"""
    requirements_list = []

    with open('requirements.txt') as requirements:
        for install in requirements:
            requirements_list.append(install.strip())

    return requirements_list

long_description = """"

Parallel Foreach Submodule
==========================

Parallel Foreach Submodule (PFS) is a tool for “git submodule foreach”
execution in parallel.

What can I do with PFS?
~~~~~~~~~~~~~~~~~~~~~~~

-  Execute git submodule foreach in parallel
-  Use it from terminal when it is installed
-  Multiplatform execution (it is developed in Python)

Installation
~~~~~~~~~~~~

You can install or upgrade PFS with:

``$ pip install pfs --upgrade``

Or you can install from source with:

.. code:: bash

   $ git clone https://github.com/RDCH106/parallel_foreach_submodule.git --recursive
   $ cd parallel_foreach_submodule
   $ pip install .

Quick example
~~~~~~~~~~~~~

.. code:: bash

   $ pfs -p "D:\project" -c "git pull origin" -j 8

The example executes command ``git pull origin`` for each submdoule in
``D:\project`` using 8 threads.
    """


setup(
    name = 'pfs',
    packages = ['parallelforeachsubmodule'],
    install_requires = requirements(),
    version = metadata.get_version(),
    license = 'LGPL v3',
    description = 'Tool for "git submodule foreach" execution in parallel ',
    long_description= long_description,
    author = metadata.get_author(),
    author_email = 'contact@rdch106.hol.es',
    url = 'https://github.com/RDCH106/parallel_foreach_submodule',
    download_url = 'https://github.com/RDCH106/parallel_foreach_submodule/archive/v'+metadata.get_version()+'.tar.gz',
    entry_points={
        'console_scripts': ['pfs=parallelforeachsubmodule.main:main'],
    },
    keywords = 'background console windows gnu-linux',
    classifiers = ['Programming Language :: Python',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6'],
)
