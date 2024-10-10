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
        'jinja2>=3.1.4',
        'requests>=2.32.3',
        'watchdog>=5.0.3',       # Updated to a compatible version
        'python-docx>=1.1.2',
        'ollama'
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
