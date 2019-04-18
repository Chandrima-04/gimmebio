from setuptools import setup

microlib_name = 'gimmebio.assembly'

requirements = [
    'pandas',
    'capalyzer',
]

setup(
    name=microlib_name,
    version='0.4.0',
    author='David Danko',
    author_email='dcdanko@gmail.com',
    license='MIT license',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    namespace_packages=['gimmebio'],
    packages=[microlib_name],
    install_requires=requirements,
)
