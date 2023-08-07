from setuptools import setup

setup(
    name='smartConvDS',
    version='0.2a',
    description='Data Conversion and Docker Image Generation Tool',
    author='Tarik Abu Mukh',
    author_email='t_abu20@cs.uni-kl.de',
    url='https://github.com/tmukh',
    download_url='https://github.com/tmukh/ds2dc/archive/refs/tags/Pre-Release.tar.gz',
    license='MPL-2.0',
    packages=['smartConvDS'],
    install_requires=[
        'networkx',
        'pandas'
        'PyYAML',
        'setuptools'

    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.6',
    ],
)