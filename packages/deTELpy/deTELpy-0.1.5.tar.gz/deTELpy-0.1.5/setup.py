import io
from setuptools import setup


def README():
    with io.open('README.md', encoding='utf-8') as f:
        readme_lines = f.readlines()

    return ''.join(readme_lines)
README = README()  # NOQA

setup(
    name='deTELpy',
    version='0.1.5',
    description='Python package of the deTEL translation error detection pipeline from mass-spectrometry data',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://git.mpi-cbg.de/atplab/detelpy',
    author='Cedric Landerer',
    author_email='landerer@mpi-cbg.de',
    license='BSD 2-clause',
    packages=['deTEL', 'deTEL.eTEL', 'deTEL.mTEL', 'deTEL.utility'],
    include_package_data=True,
    install_requires=['pandas==1.3.5',
                      'numpy',
                      'dataclasses>=0.6',
                      'pathlib>=1.0.1',
                      'biopython>=1.81',
                      'numba>=0.57.1',
                      'scipy>=1.7.3',
                      'tqdm>=4.65.0',
                      'seaborn>=0.12.2',
                      'matplotlib>=3.5.3',
                      'gooey>=1.0.7',
                      'python-dateutil'
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
