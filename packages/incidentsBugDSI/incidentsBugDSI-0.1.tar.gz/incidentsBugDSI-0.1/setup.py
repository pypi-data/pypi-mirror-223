from setuptools import setup

setup(
    name='incidentsBugDSI',
    packages=['incidentsBugDSI'],
    version='0.1',
    long_description=open("README.rst", "r").read(),
    description='Gestión de incidencias de tipo bug',
    author='DSI.',
    author_email='jairo@dsinno.io',
    url='https://dsinno@bitbucket.org/rpa-s/libreriagestionincidenciastipobug.git',
    classifiers=[],
    license='MIT',
    install_requires=[
        'pika'
    ]
)
