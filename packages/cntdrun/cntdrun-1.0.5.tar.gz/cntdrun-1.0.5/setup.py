from setuptools import setup

setup(
    name='cntdrun',
    version='1.0.5',
    author='gzj',
    author_email='gzj00@outlook.com',
    description='A countdown running program tool',
    long_description='A countdown running program tool',
    long_description_content_type="text/markdown",
    py_modules=['cntdrun'],
    install_requires=[
        'pyqt5',
    ],
    entry_points={
        'console_scripts': [
            'cntdrun = cntdrun:main',
        ],
    },
)
