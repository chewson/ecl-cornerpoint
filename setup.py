from setuptools import setup
import os.path

setup(
    name='cp_gen',

    version='2018.03',

    packages=['cp_gen'],

    package_data={},

    url='',

    license='Reservoir Concepts',

    author='chewson',

    author_email='chris.hewson@reservoirconcepts.com',

    description="Corner Point Grid Generating Tool",

    scripts=[os.path.join('bin', 'cp_gen')],

    install_requires=['scipy']
)