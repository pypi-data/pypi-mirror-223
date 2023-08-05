from distutils.core import setup


with open("README.md", "r") as rd:
  long_desc = rd.read()


setup(
  name = 'sightvision',         # How you named your package folder (MyLib)
  packages = ['sightvision'],   # Chose the same as "name"
  version = '0.2.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This is a Computer vision package that makes its easy to run Image processing and AI functions.',   # Give a short description about your library
  long_description=long_desc,
  long_description_content_type='text/markdown',
  author = 'Leonardi Melo',                   # Type in your name
  author_email = 'opensource.leonardi@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/rexionmars/SightVision',   # Provide either the link to your github or to your website
  #download_url = 'https://github.com/rexionmars/SightVision/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['Computervision', 'Imageutils', 'Imageprocessing'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'opencv-python',
          'mediapipe',
          'tensorflow',
          'serial',
          'numpy',
          'pyserial',
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
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)