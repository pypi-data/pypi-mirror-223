from setuptools import setup, find_packages

setup(
    name='NiantongEEG',
    version='0.1.3.11',
    packages=find_packages(),
    package_data={'': ['eCon_*.pyd']},
    python_requires='==3.11.*',
    zip_safe=False,
)
