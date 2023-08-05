from setuptools import setup, find_packages

setup(
    name='SRID300002',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # Bağımlılıklarınızı buraya ekleyin
    ],
    description='This project aim to convert wgs84 to local coordinate system like TUREF tm30',
    author='Kemal Öz',
    author_email='ikemaloz7@gmail.com',
    url='https://github.com/ozk17/Convert_WGS84_Local',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
