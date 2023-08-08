from distutils.core import setup
setup(
  name = 'lopl_package',         # How you named your package folder (MyLib)
  packages = ['lopl_package'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = "LOPL stands for Leo's Own Programming Language and can be used to help visualize behind the scene functionality in your code. I created this programming language while reading Crafting Interpreters. It is a mix of C and JavaScript, but uses the Python Virtual Machine.",
  author = 'Leo Carten',                   # Type in your name
  author_email = 'lcarten14@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/leocarten/lopl',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/leocarten/lopl/archive/refs/tags/v_01.tar.gz', 
  keywords = ['code visualizer', 'bytecode'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'dis'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)