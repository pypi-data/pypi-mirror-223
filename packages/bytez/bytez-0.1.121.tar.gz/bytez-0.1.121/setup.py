from setuptools import setup, find_packages


packages = find_packages()


setup(
    name='bytez',
    version='0.1.121',
    packages=packages,
    install_requires=[
        'charset-normalizer==3.1.0',
        'idna==3.4',
        'requests==2.28.2',
        'urllib3==1.26.15',
    ],
    author='Bytez',
    author_email='nawar@bytez.com',
    description='Client for interfacing with the Bytez ML playground.',
    long_description='Client for interfacing with the Bytez ML playground.\n\nTo request an API key, please visit https://bytez.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],

)
