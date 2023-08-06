#!/usr/bin/env python3
# region Imports
import pathlib, zipfile
import os
import sys
from setuptools import find_packages, setup

# endregion
# region Basic Information
here = os.path.abspath(os.path.dirname(__file__))
py_version = sys.version_info[:2]
NAME = "andak"
AUTHOR = 'Miles Frantz'
EMAIL = 'frantzme@vt.edu'
DESCRIPTION = 'My short description for my project.'
GH_NAME = "franceme"
URL = f"https://github.com/{GH_NAME}/{NAME}"
long_description = pathlib.Path(f"{here}/README.md").read_text(encoding='utf-8')
REQUIRES_PYTHON = '>=3.8.0'
RELEASE = "?"
entry_point = f"src.{NAME}"
VERSION = "0.0.4"

def zip_program(outputName:str = f"{NAME}.zip"):
	#http://blog.ablepear.com/2012/10/bundling-python-files-into-stand-alone.html
	if os.path.exists(outputName):
		os.system(f"rm {outputName}")

	zipf = zipfile.ZipFile(outputName, 'w', zipfile.ZIP_DEFLATED)
	success = 0
	try:
		zipf.write("setup.py")
		zipf.write("README.md")
		zipf.write("__main__.py")
		for root, dirs, files in os.walk('src/'):
			for file in [x for x in files if not x.endswith('.pyc')]:
				ending_path = os.path.relpath(os.path.join(root, file), os.path.join('src/', '..'))
				zipf.write(
					os.path.join(root, file),
					ending_path
				)
		print(f"Successful: {outputName}")
	except Exception as e:
		print(f"Failing the exception check: {e}")
		success = 1
	zipf.close()
	return(success)

# endregion
# region CMD Line Usage
def selfArg(string):
	return __name__ == "__main__" and len(
		sys.argv) > 1 and sys.argv[0].endswith('/setup.py') and str(
			sys.argv[1]).upper() == str(string).upper()

if selfArg('install'):
	sys.exit(os.system('python3 -m pip install -e .'))
elif selfArg('upload'):
	grab_version(True)
	sys.exit(os.system(f"{sys.executable} setup.py sdist && {sys.executable} -m twine upload --skip-existing dist/*"))
elif selfArg('zip'):
	sys.exit(zip_program())
# endregion
# region Setup

setup(
	name=NAME,
	version=VERSION,
	description=DESCRIPTION,
	long_description=long_description,
	long_description_content_type='text/markdown',
	author=AUTHOR,
	author_email=EMAIL,
	command_options={
	},
	python_requires=REQUIRES_PYTHON,
	url=URL,
	packages=find_packages(
		exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
	entry_points={
	},
	install_requires=[
		"ephfile", "hugg", "mystring", "github-clone", "PyGithub", "pause"
	],
	include_package_data=True,
	classifiers=[
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.8',
	],
)
# endregion
