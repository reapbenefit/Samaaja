from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in samaaja/__init__.py
from samaaja import __version__ as version

setup(
	name="samaaja",
	version=version,
	description="Samaaja is an open source software solution for rapidly building location based civic services connected with volunteer, human interactions. It comes with all necessary UI and management features and can be easily extended into web applications and external mobile apps and systems via built-in APIs.",
	author="FOSSUnited ReapBenefit Impactyaan ",
	author_email="ankit@impactyaan.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
