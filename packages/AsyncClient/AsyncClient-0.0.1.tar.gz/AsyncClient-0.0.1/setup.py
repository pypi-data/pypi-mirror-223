from setuptools import setup, find_packages

setup(name="AsyncClient",
      version="0.0.1",
      description="Chat with encryption",
      author="Ekaterina Eranova",
      author_email="kteranova@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
