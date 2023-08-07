import codecs
import os

from setuptools import find_namespace_packages, setup


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


def parse_requirements(requirements):
    with open(requirements) as requirements_file:
        return [
            line.strip('\n') for line in requirements_file
            if line.strip(' \t\n') and not line.startswith('#')
            and not line.startswith('-c')

        ]


setup(
    name='howso-engine',
    version=get_version("howso/community/__init__.py"),
    description=('Howso Engine and Scikit Estimator for the interpretable Machine Learning '
                 'and Artificial Intelligence API.'),
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Howso Incorporated',
    author_email='support@howso.com',
    license='GNU Affero General Public License v3',
    license_files=('LICENSE.txt', ),
    classifiers=[
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: MacOS',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows 11',
        'Operating System :: POSIX :: Linux',
    ],
    keywords=[
        'machine learning',
        'artificial intelligence',
    ],
    install_requires=parse_requirements('requirements-engine.in') + parse_requirements('requirements.in'),
    project_urls={
        'Documentation': 'https://docs.community.howso.com/'
    },
    python_requires='>=3.8',
    url='https://howso.com',
    packages=find_namespace_packages(include=['howso.*']),
    include_package_data=True,
)
