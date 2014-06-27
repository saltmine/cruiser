from setuptools import setup, find_packages


setup(
  name='cruiser',
  author='Steve Heinz',
  author_email='steve@keep.com',
  version='0.0.1',
  packages=find_packages(exclude=['tests*']),
  include_package_data=True,
  package_data={'cruiser': ['cruiser/etc/*']},
  url='http://keep.com',
  license='Private to keep.com',
  description='product ranking service',
  long_description=open('README').read(),
  zip_safe=False,
  install_requires=open('pip_requirements.txt').readlines(),
  dependency_links=open('dependency_links.txt').readlines(),
  entry_points={
    'console_scripts': [
      'cruiser = cruiser.commands:main',
      ]
    }
)
