from setuptools import setup, find_packages

setup(
    name='ccrypto',
    version='0.0.6',
    license='MIT',
    author="Python",
    author_email='pawel.lachowicz@quantatrisk.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/quantatrisk/ccrypto',
    keywords='cryptocurrency crypto python derivatives',
    long_description_content_type='text/x-rst',
    long_description='Crypto-Finance Python library for crypto markets and data analysis by QuantAtRisk.com',
    install_requires=[
          'requests',
          'python-binance==1.0.17',
          'numpy',
          'pandas',
          'matplotlib'
      ],

)
