# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                                                           #
#   This file was created by: Alberto Palomo Alonso         #
# Universidad de Alcalá - Escuela Politécnica Superior      #
#                                                           #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='newsegmentation',
    version='0.3.2',
    author='Alberto Palomo Alonso',
    author_email='a.palomo@uah.es',
    description='Package for news segmentation architecture.',
    keywords='deeplearning, ml, api',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/iTzAlver/newsegmentation.git',
    project_urls={
        'Documentation': 'https://github.com/iTzAlver/newsegmentation/blob/master/README.md',
        'Bug Reports':
        'Bug Tracker = https://github.com/iTzAlver/newsegmentation/issues',
        'Source Code': 'https://github.com/iTzAlver/newsegmentation.git',
        # 'Funding': '',
        # 'Say Thanks!': '',
    },
    package_dir={'': 'newsegmentation'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Researchers',
        'Topic :: Software Development :: Build Tools',

        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache License'
    ],
    python_requires='>=3.6',
    # install_requires=['Pillow'],
    extras_require={
        'dev': ['check-manifest'],
    },
)
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                        END OF FILE                        #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
