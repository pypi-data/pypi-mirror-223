from setuptools import setup, find_packages

setup(
    name='focosql',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'python-dotenv',
        'mysql-connector-python',
    ],
    author='FocoGrafico',
    author_email='enrique.dealba@focograficomx.com'
)
