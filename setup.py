from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='pystiler',
      version='0.1.2',
      description='Python simple tiler for non-tiling window managers',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.6',
        'Topic :: Desktop Environment :: Window Managers',
      ],
      keywords='window-manager tiling wm command-line cli',
      url='http://github.com/riley-martine/pystiler',
      author='Riley Martine',
      author_email='riley.martine.0@gmail.com',
      license='MIT',
      packages=['pystiler'],
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False)