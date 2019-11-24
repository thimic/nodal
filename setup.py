
import re
import setuptools

from git import Repo
from packaging import version


with open('README.md', 'r') as fh:
    long_description = fh.read()


def get_release_version_from_tag():
    repo = Repo()
    pattern = re.compile(r'v(?P<version>\d+\.\d+\.\d+)')
    versions = [
        pattern.match(t.name).groupdict().get('version') for t in repo.tags
        if pattern.match(t.name)
    ]
    if not versions:
        raise RuntimeError('No git tags found!')
    versions.sort(key=lambda x: version.parse(x))
    return versions[-1]


setuptools.setup(
    name='nodal',
    version=get_release_version_from_tag(),
    author='Michael Thingnes',
    author_email='thimic@gmail.com',
    description='An execution graph for Python tasks',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/thimic/nodal',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    setup_requires=['wheel', 'pyyaml'],
)
