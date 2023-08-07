from setuptools import find_packages, setup
setup(
    name='pyhman',
    packages=find_packages(include=['pyhman']),
    version='1.0.2',
    description='Python library to control the HMan robot',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Alexis Devillard',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)