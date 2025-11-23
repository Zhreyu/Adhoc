from setuptools import setup, find_packages

setup(
    name='adhoc-python',
    version='1.0.1',  # Increment the version number appropriately
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'adhoc.templates': ['*.tex', '*.md', '*.docx'],
    },
    entry_points={
        'console_scripts': [
            'adhoc=adhoc.adhoc:main',
        ],
    },
    install_requires=[
        'jinja2>=3.1.6',
        'requests>=2.32.5',
        'watchdog>=6.0.0',
        'python-docx>=1.2.0',
        'ollama>=0.6.1'
        # Removed 'argparse' as it's part of the standard library for Python >=3.2
    ],
    author='Shreyas S',
    author_email='Zhreyas1@example.com',
    description='Auto Document Codebase Changes in LaTeX, Markdown, or Word',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Zhreyu/adhoc',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Update if using a different license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
