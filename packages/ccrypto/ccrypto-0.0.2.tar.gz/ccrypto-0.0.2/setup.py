from setuptools import setup, find_packages

setup(
    name='ccrypto',
    version='0.0.2',
    license='MIT',
    author="Python",
    author_email='pawel.lachowicz@quantatrisk.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/quantatrisk/ccrypto',
    keywords='cryptocurrency crypto python derivatives',
    install_requires=[
          'requests',
          'python-binance',
          'numpy',
          'pandas',
          'matplotlib'
      ],

)
