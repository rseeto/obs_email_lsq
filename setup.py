from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='obs_email_lsq',
    version='0.1.0',
    description='Send OBS emails containing LSQs',
    long_description=readme,
    author='Ryan Seeto',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
