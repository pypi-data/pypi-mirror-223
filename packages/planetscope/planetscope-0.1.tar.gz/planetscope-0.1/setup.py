from setuptools import setup

setup(
    # Needed to silence warnings
    name='planetscope',
    url='https://github.com/ankurk017/planet_utilities',
    author='Ankur Kumar',
    author_email='ankurk017@gmail.com',
    # Needed to actually package something
    packages=['planetscope'],
    # Needed for dependencies
    install_requires=open('requirements.txt').read().split('\n')[:-1],
    # *strongly* suggested for sharing
    version='0.1',
    license='MIT',
    description='The planetscope package is a tool specifically designed to read and plot data from the PlanetScope satellite imaging system.',
    # We will also need a readme eventually (there will be a warning)
    long_description=open('README.md').read(),
)
