import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 's1290018_learn',
    version = '1.0.1',
    description = 'project is complete.',
    long_description = long_description,
    author = 's1290018',
    url = 'https://github.com/curamubo/s1290018_learn',
    packages = setuptools.find_packages(),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    license = 'GPLv3',
    long_description_content_type = 'text/markdown',
    install_requires = [
        'plotly',
        'pandas',
    ],
    python_requires = '>=3.5',
)
