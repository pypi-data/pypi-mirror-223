from setuptools import setup, find_packages

setup(name="sun_client_proj",
      version="0.0.2",
      description="sun_client_proj",
      author="zSusnet",
      author_email="z2x6csunset@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
