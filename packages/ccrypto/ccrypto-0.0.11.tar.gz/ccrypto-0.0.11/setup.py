import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.11'
PACKAGE_NAME = 'ccrypto'
AUTHOR = 'Pawel Lachowicz'
AUTHOR_EMAIL = 'pawel.lachowicz@quantatrisk.com'
URL = 'https://github.com/quantatrisk/ccrypto'

LICENSE = 'MIT'
DESCRIPTION = 'Crypto-Finance Python library for crypto markets and data analysis by QuantAtRisk.com'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'numpy',
      'pandas',
      'python-binance==1.0.17',
      'matplotlib',
      'requests'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )
