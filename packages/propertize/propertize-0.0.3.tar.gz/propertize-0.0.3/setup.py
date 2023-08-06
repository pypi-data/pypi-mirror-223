"""
Propertize
-------------

Unwrap custom @properties so your IDE understands them.
"""

# import os

from setuptools import setup, find_packages


# on_rtd = os.getenv('READTHEDOCS') == 'True'
# if on_rtd:
#     requirements.append('sphinxcontrib-napoleon')
#     requirements.append('Pallets-Sphinx-Themes')


setup(
    name="propertize",
    version="0.0.3",
    author="Philip Dowie",
    author_email="philip@jnawk.nz",
    description="Unwrap custom properties",
    url="https://github.com/jnawk/propertize",
    license="MIT",
    long_description=__doc__,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    # zip_safe=False,
    include_package_data=True,
    # platforms="any",
    install_requires=[],
    setup_requires=["wheel"],
    # extra_requirements={"docs": ["sphinx==1.8.3"]},
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
