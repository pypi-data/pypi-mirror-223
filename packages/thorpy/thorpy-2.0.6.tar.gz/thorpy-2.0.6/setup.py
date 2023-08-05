from setuptools import find_packages, setup

setup(name='thorpy',
      version='2.0.6',
      description='GUI library for pygame',
      long_description='ThorPy is a non-intrusive, straightforward GUI kit for Pygame.',
      author='Yann Thorimbert',
      author_email='yann.thorimbert@gmail.com',
      url='http://www.thorpy.org/',
      keywords=['pygame', 'gui', 'menus', 'buttons', 'widgets', 'user interface', 'toolkit'],
      packages=find_packages(),
      include_package_data=True,
      package_data={
          'thorpy': ['data/*'],
      },
      license='MIT')
