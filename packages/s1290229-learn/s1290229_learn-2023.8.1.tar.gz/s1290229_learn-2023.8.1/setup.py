import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='s1290229_learn',
    version='2023.08.01',
    author='Wakatsuki Yuya',
    author_email='s1290229@u-aizu.ac.jp',
    description='This software is being developed at the University of Aizu, Aizu-Wakamatsu, Fukushima, Japan',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    url='https://github.com/WAKATSUKIYuya/s1290229_learn.git',
    license='GPLv3',
    install_requires=[
        'psutil',
        'pandas',
        'plotly',
        'matplotlib',
        'resource',
        'validators',
        'urllib3',
        'Pillow',
        'numpy',
        'pami',
    ],
    extras_require={
        'pgu': ['cupy', 'pycuda'],
        'spark': ['pyspark'],
        'dev': ['twine', 'setuptools', 'build'],
        'all': ['cupy', 'pycuda', 'pyspark', 'twine', 'setuptools', 'build']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
)