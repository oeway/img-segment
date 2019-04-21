from setuptools import setup, find_packages

REQUIREMENTS = ['numpy', 'Pillow', 'scikit-image', 'nested_lookup', 'read-roi', 'palettable']

setup(
    name='imgseg',
    version='0.1.0',
    description='Python modules to perform cell segmentaiton with the ImJoy plugin Anet.',
    url='http://whatever',
    author='Florian MUELLER',
    author_email='muellerf.research@gmail.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    zip_safe=False)
