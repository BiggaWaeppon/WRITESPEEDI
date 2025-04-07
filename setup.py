from setuptools import setup, find_packages

setup(
    name='writespeedi',
    version='1.0.0',
    description='A typing speed testing application',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/writespeedi',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Web version requirements
        'Flask==3.0.0',
        'Flask-SQLAlchemy==3.1.1',
        'Flask-Login==0.6.3',
        'bcrypt==4.1.2',
        'requests==2.31.0',
        
        # Console version requirements
        'colorama==0.4.6'
    ],
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
