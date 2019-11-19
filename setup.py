from distutils.core import setup

setup(
    name='SLAZTA',
    version='0.2',
    author="Ash Munro",
    author_email="anne.munro@canada.com",
    packages=['SLAZTA',],
    license='MIT License',
    url='https://github.com/CSBP-CPSE/SLA-ZTA/',
    description = 'SLAZTA is a tool to create self-contained areas from commuting data.',
    long_description=open('README.txt').read(),
)