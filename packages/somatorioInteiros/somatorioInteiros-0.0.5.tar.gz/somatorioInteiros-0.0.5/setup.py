from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='somatorioInteiros',
    version='0.0.5',
    license='MIT License',
    author='Joao Neto',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='joaonetoprivado2001@ufpi.edu.br',
    keywords='soma inteiros',
    description=u'Somador de numeros inteiros em uma lista',
    packages=['src'],)