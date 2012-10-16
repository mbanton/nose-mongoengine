from setuptools import setup, find_packages

setup(name='nose-mongoengine',
      version="0.1.0",
      classifiers=[
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP'],
      author='Marcelo Anton',
      author_email='marceloanton@gmail.com',
      description="A nose plugin to facilitate the creation of automated tests that access Mongo Engine structures.",
      long_description=open("README.md").read(),
      url='https://github.com/mbanton/nose-mongoengine/',
      license='BSD-derived',
      packages=find_packages(),
      install_requires=["nose", "mongoengine"],
      include_package_data=True,
      zip_safe=True,
      entry_points = {
        'nose.plugins': ['mongoengine = nose_mongoengine:MongoEnginePlugin'],
      },
)
