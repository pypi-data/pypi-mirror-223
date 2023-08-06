from setuptools import setup, find_packages
from ortei import __version__

with open("README.md", 'r', encoding='utf-8') as f:
    readme = f.read()

with open("requirements.txt", 'r', encoding='utf-8') as f:
    requires = f.read()

setup(
    name='ortei',
    version=__version__,
    description='ONNX-Runtime-Engine-Interface',
    long_description=readme,
    author='404Vector',
    author_email='tiryul@gmail.com',
    url='https://github.com/404Vector/Package.ONNX-Runtime-Engine-Interface/tree/main',
    packages=find_packages(exclude=[]),
    install_requires=requires,
    keywords=['404Vector', 'ortei', ],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)