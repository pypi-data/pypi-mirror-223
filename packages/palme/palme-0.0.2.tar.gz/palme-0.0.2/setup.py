from setuptools import setup, find_packages

setup(
  name = 'palme',
  packages = find_packages(exclude=['examples']),
  version = '0.0.2',
  license='MIT',
  description = 'palme - Pytorch',
  author = 'Kye Gomez',
  author_email = 'kye@apac.ai',
  url = 'https://github.com/kyegomez/palme',
  long_description_content_type = 'text/markdown',
  keywords = [
    'artificial intelligence',
    'attention mechanism',
    'transformers'
  ],
  install_requires=[
    "torch"
    "lion-pytorch",
    "numpy",
    "einops",
    "accelerate",
    "transformers",
    "SentencePiece",
    "datasets",
    "matplotlib",
    "deepspeed",
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)