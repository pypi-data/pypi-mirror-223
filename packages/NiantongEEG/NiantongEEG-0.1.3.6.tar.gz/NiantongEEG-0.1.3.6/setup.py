from setuptools import setup, find_packages

setup(
    name='NiantongEEG',
    version='0.1.3.6',
    packages=find_packages(),
    package_data={'': ['eCon_*.pyd']},
    python_requires='==3.6.*',
    zip_safe=False,
)
