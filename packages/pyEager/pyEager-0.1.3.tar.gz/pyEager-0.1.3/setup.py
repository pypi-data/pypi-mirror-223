from distutils.core import setup
setup(
  name = 'pyEager',
  packages = ['pyEager'],
  version = '0.1.3',
  license='MIT',
  description = 'A simple package to read in eager results.',
  long_description=open('README.md').read(),
  author = 'Thiseas C. Lamnidis',
  author_email = 'thisseass@gmail.com',
  url = 'https://github.com/TCLamnidis/pyEager',
  download_url = 'https://github.com/TCLamnidis/pyEager/archive/refs/tags/0.1.3.tar.gz',
  keywords = ['python', 'pandas', 'nf-core', 'eager', 'nf-core/eager', 'ancient DNA' ],
  python_requires=">=3.6",
  install_requires=[
          'pandas',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    # 'Intended Audience :: Developers',      # Define that your audience are developers
    # 'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)