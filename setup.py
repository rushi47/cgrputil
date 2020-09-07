import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cgrputil", 
    version="1.0.1",
    author="Rushikesh Butley",
    author_email="rushikeshbutley@gmail.com",
    description="Package to calculate cpu utilisation in cgroups",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rushi47/cgrputil",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Environment :: Console",
        "Environment :: Other Environment",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: System", 
    ],
    python_requires='>=2.7',
    data_files=[('LICENSE', ['LICENSE']),
                ('README', ['README.md']),
                ]
)
