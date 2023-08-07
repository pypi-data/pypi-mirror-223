from setuptools import setup

setup(
    name='revwhox',
    version='1.1.1',
    py_modules=['revwhox'],
    url='https://github.com/null3yte/revwhox',
    license='',
    author='null3yte',
    author_email='nullmad.eb00@gmail.com',
    long_description='a',
    long_description_content_type='text/markdown',
    description='Find domain names owned by an individual or company using this tool.',
    entry_points={
        'console_scripts': [
            'revwhox = revwhox:main'
        ]
    },
    install_requires=[
        'setuptools~=65.5.0',
        'aiohttp~=3.8.4',
        'bs4~=0.0.1',
        'beautifulsoup4~=4.12.2',
        'selenium~=4.10.0',
    ]
)
