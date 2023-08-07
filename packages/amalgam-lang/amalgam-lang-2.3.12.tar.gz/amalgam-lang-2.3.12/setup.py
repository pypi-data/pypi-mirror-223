import codecs
import os.path

from setuptools import setup


def read(rel_path):
    """Read a file and return its contents."""
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    """Get the version of this package."""
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


def parse_requirements(requirements):
    """Parse requirements for this package."""
    with open(requirements) as requirements_file:
        return [
            line.strip('\n') for line in requirements_file
            if line.strip(' \t\n') and not line.startswith('#')
        ]


# Small piece of formatting required to use requirements-dev.in as extra_require
dev_reqs = parse_requirements('requirements-dev.in')
dev_reqs.remove('-c requirements.in')

setup(
    name='amalgam-lang',
    version=get_version("amalgam/__init__.py"),
    packages=['amalgam'],
    url='https://howso.com',
    license='GNU Affero General Public License v3',
    license_files=('LICENSE.txt', ),
    author='Howso Incorporated',
    author_email='support@howso.com',
    # Note - this is a library file - so not using the pinned versions in requirements.txt
    install_requires=parse_requirements('requirements.in'),
    extras_require={
        'dev': dev_reqs
    },
    include_package_data=True,
    description='A direct interface with Amalgam compiled DLL or so.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    project_urls={
        'Documentation': 'https://docs.community.howso.com/'
    },
    keywords=[
        'artificial intelligence',
        'machine learning',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
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
)
