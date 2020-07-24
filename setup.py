from setuptools import setup

setup(
    name='scc',
    version='0.1',
    py_modules=['scc'],
    install_requires=[
        'click',
        'requests',
        'win10toast',
        'click_shell',
    ],
    entry_points='''
        [console_scripts]
        scc=scc:cli
    ''',
)
