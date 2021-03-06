from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license_ = f.read()

setup(
    name='econ_watcher_reader',
    version='0.0.1',
    description='Web scraper to get economy watcher data from Cabinet Office of Japan.',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Yuta Sugiura',
    author_email='ced4141@me.com',
    install_requires=['numpy', 'pandas', 'xlrd', 'requests', 'bs4'],
    url='https://github.com/si4141/scraper_for_economy_watcher',
    license=license_,
    packages=find_packages(exclude=('tests', 'docs')),
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 4 - Beta',
    ]
)