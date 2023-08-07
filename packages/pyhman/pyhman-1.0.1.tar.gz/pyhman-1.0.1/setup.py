from setuptools import find_packages, setup
setup(
    name='pyhman',
    packages=find_packages(include=['pyhman']),
    version='1.0.1',
    description='My first Python library',
    author='Alexis Devillard',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)