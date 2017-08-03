from setuptools import setup

setup(name='pystiler',
      version='0.1.1',
      description='Python simple tiler for non-tiling window managers',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.6',
        'Topic :: Desktop Environment :: Window Managers',
      ]
      keywords='window-manager tiling wm command-line cli',
      url='http://github.com/riley-martine/pystiler',
      author='Riley Martine',
      author_email='riley.martine.0@gmail.com',
      license='MIT',
      packages=['pystiler'],
      include_package_data=True,
      zip_safe=False)
