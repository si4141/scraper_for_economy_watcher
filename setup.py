from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license_ = f.read()

setup(
    name='scraper_for_economy_watcher',
    version='0.0.1',
    description='Web scraper to get economy watcher data from Cabinet Office of Japan.',
    long_description=readme,
    author='Yuta Sugiura',
    author_email='soeur.si.4141@gmail.com',
    install_requires=['numpy'],
    url='',
    license=license_,
    packages=find_packages(exclude=('tests', 'docs'))
)