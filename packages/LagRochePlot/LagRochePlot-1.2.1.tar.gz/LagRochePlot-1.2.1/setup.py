from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
      name = 'LagRochePlot',
      version = '1.2.1',
      license = 'MIT',
      description = 'Herramienta gráfica para visualizar los puntos de Lagrange y potencial de Roche.',
      long_description = long_description,
      long_description_content_type = 'text/markdown',
      author = 'Thomas Salazar, Esteban Sanchez, Sebastian Lopez, Andres Rumillanca',
      install_requires = ['numpy', 'matplotlib', 'pyastronomy'],
      url = 'https://github.com/Thomas-thief/LagRochePlot',
      )
