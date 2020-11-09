from setuptools import setup

setup(
    name="codeseq",
    version='0.1',
    py_modules=['codeseq'],
    install_requires=[
        'sys',
        'ast',
        'pathlib',
        'itertools',
        'tokenize',
        'pandas',
        'click',
        'collections',
        'tqdm'
    ],
    entry_points='''
        [console_scripts]
        codeseq=codeseq:cli
    ''',
)
