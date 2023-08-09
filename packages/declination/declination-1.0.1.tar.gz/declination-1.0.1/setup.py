from setuptools import setup, find_packages

setup(
    name='declination',
    version='1.0.1',
    description='Calculates declination given a latitude and longitude.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    author='Andrew Humphrey',
    author_email='digiwhale.humphrey@gmail.com',
    license='MIT',
    url='https://github.com/DigiWhale/declination',
    install_requires=[
        # No third-party dependencies based on the imports you've mentioned
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: GIS",
    ],
)
