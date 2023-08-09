from setuptools import setup, find_packages

setup(
    name='declination',
    version='1.0',
    description='Calculates declination given a latitude and longitude.',
    packages=find_packages(),
    author='Andrew Humphrey',  # Replace with your name
    author_email='digiwhale.humphrey@gmail.com',  # Replace with your email
    license='MIT',  # Assuming MIT, but replace if different
    url='https://github.com/DigiWhale/declination',  # Replace with your repository or homepage URL
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
