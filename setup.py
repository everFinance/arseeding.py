import setuptools

setuptools.setup(
    name='arseeding',
    version='0.0.6',
    packages=['arseeding',],
    license='MIT',
    description = 'Python sdk for arseeding',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author = 'xiaojay',
    author_email = 'xiaojay@gmail.com',
    install_requires=['everpay', 'requests', 'web3', 'python-jose', 'arweave-python-client', 'eth_account', 'fastavro', 'colorama'],
    url = 'https://github.com/everFinance/arseeding.py',
    download_url = 'https://github.com/everFinance/arseeding.py/archive/refs/tags/v0.0.6.tar.gz',
    scripts=['bin/arseed'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
