from setuptools import setup, find_packages
import os

# Get the directory containing this setup.py file
here = os.path.dirname(os.path.abspath(__file__))

# Read requirements from files
def read_requirements(file_path):
    with open(os.path.join(here, file_path)) as f:
        return f.read().splitlines()

setup(
    name='writespeedi',
    version='1.0.0',
    description='A typing speed testing application',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/writespeedi',
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements('requirements.txt'),
    extras_require={
        'web': read_requirements(os.path.join('Web Version', 'requirements_web.txt')),
        'console': read_requirements(os.path.join('Console Version', 'requirements.txt'))
    },
    entry_points={
        'console_scripts': [
            'writespeedi-web=Web Version.app:main',
            'writespeedi-console=Console Version.CONSOLE-APP_CONSOLE-APP.CONSOLE-APP_main:main'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
