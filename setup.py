from setuptools import setup

setup(
    name="pycodeseq",
    version='0.2.0',
    py_modules=['pycodeseq'],
    python_requires='>=3.8',  # the end_line no in AST is necessary
    install_requires=[
        'pandas==1.1.4',
        'click==7.1.2',
        'tqdm==4.51.0'
    ],
    entry_points='''
        [console_scripts]
        pycodeseq=pycodeseq.pycodeseq:count
        size_reduce=pycodeseq.size_reduce:clean
    ''',
)
