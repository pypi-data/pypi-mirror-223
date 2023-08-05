import os

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as wfile:
    README = wfile.read()

setup(
    name="redis_exec_retry",
    version="0.0.2",
    description="redis-py that handles errors better.",
    long_description=README,
    url="https://github.com/geonyoro/redis-exec-retry",
    author="George Nyoro",
    author_email="geonyoro@gmail.com",
    license="MIT License",
    py_modules=["redis_exec_retry"],
    install_requires=["redis>=4.6.0"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    package_dir={"": "src"},
)
