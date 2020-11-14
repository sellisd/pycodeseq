from setuptools import setup

setup(
    name="codeseq",
    version='0.220',
    py_modules=['codeseq'],
    install_requires=[
        'pandas==1.1.4',
        'click==7.1.2',
        'tqdm==4.51.0'
    ],
    entry_points='''
        [console_scripts]
        codeseq=codeseq.codeseq:count
    ''',
)
