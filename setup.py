from setuptools import setup, find_packages

setup(
    name='shadeform',
    version='0.1.0',
    description='A Python SDK for the Shadeform API.',
    author='Shadeform',
    author_email='support@shadeform.ai',
    url='https://github.com/shadeform/shadeform-python',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
    ],
    extras_require={
        'dev': [
            'pytest>=6.2.4',
            'flake8>=3.9.2',
            'mypy>=0.910',
            'black>=21.6b0',
            'sphinx>=4.0.2',
            'sphinx-rtd-theme>=0.5.2',
            'pytest-cov>=2.12.1',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    project_urls={
        'Documentation': 'https://docs.shadeform.ai',
        'Source': 'https://github.com/shadeform/shadeform-python',
        'Issues': 'https://github.com/shadeform/shadeform-python/issues',
    },
)