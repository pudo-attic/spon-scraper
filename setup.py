from setuptools import setup, find_packages

setup(
    name='spon',
    version='0.1',
    description="Spiegel Online content processing.",
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        ],
    keywords='spon spiegel scraping',
    author='Friedrich Lindenberg',
    author_email='friedrich@pudo.org',
    url='http://github.com/pudo/spon',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=[],
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        'dataset>=0.3.6',
        'requests>=1.2',
        "lxml",
        "python-dateutil"
    ],
    tests_require=[],
    entry_points={
        'console_scripts': []
    }
)
