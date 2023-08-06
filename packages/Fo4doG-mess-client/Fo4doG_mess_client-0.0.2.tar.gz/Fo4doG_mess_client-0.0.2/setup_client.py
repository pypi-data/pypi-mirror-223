from setuptools import setup, find_packages

setup(name="Fo4doG_mess_client",
      version="0.0.2",
      description="Fo4doG_mess_client",
      author="Ivan Ivanov",
      author_email="iv.iv@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
