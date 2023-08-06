
from distutils.core import setup
setup(
  name = 'tokotime',         # How you named your package folder (MyLib)
  version = '0.14',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = "Tokopedia Data Science Forecasting Reusable Package",   # Give a short description about your library
  author = 'Alan Choon',                   # Type in your name
  author_email = 'alan.yu@tokopedia.com',      # Type in your E-Mail
  url = 'https://github.com/tokopedia/forecasting-platform-utils',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/tokopedia/forecasting-platform-utils/archive/refs/tags/v_014.tar.gz',
  keywords = ['Forecasting', 'Machine Learning'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
        'darts',
        'lightgbm',
        'mpire',
        'numpy',
        'optuna',
        'pandarallel',
        'pandas',
        'pmdarima',
        'protobuf',
        'pytz',
        'scikit_learn',
        'scikit_lego',
        'sklego',
        'sktime',
        'statsmodels',
        'threadpoolctl',
        'tqdm',
        'ipywidgets'
      ],
  package_dir={"": "src"}, 
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.7',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
  ],
)