import glob
import pathlib
from distutils.util import convert_path
from setuptools import setup

with pathlib.Path('requirements.txt').open() as r:
  install_requires = [
    str(requirement).replace('\n', '')
    for requirement
    in r.readlines()
  ]
install_requires.append('setuptools')

main_ns = {}
version = convert_path('co2_emission/version.py')
with open(version) as f:
  exec(f.read(), main_ns)

setup(
  name='cerc-co2-emission',
  version=main_ns['__version__'],
  description="CERC co2 emission contains the basic co2 emission calculation per CERC-Hub building",
  long_description="CERC co2 emission contains the basic co2 emission calculation per CERC-Hub building",
  classifiers=[
    "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
  ],
  include_package_data=True,
  packages=['co2_emission'],
  setup_requires=install_requires,
  install_requires=install_requires,
  data_files=[
    ('co2_emission', glob.glob('requirements.txt'))
  ]
)
