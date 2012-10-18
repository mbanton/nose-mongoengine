from setuptools import setup, find_packages

DESCRIPTION = 'A nose plugin to facilitate the creation of automated tests' +\
              ' that access Mongo Engine structures.'

f = open("README.rst")
try:
    try:
        LONG_DESCRIPTION = f.read()
    except:
        LONG_DESCRIPTION = ""
finally:
    f.close()


CLASSIFIERS = [
    'Environment :: Plugins',
    'Intended Audience :: Developers',
    'Programming Language :: Python',
    'Operating System :: OS Independent',
    'Topic :: Internet :: WWW/HTTP',
]


setup(name='nose-mongoengine',
      version="0.2.0",
      classifiers=CLASSIFIERS,
      author='Marcelo Anton',
      author_email='marceloanton@gmail.com',
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      url='https://github.com/mbanton/nose-mongoengine/',
      download_url='https://github.com/mbanton/nose-mongoengine/tarball/master',
      license='BSD-derived',
      packages=find_packages(exclude=('tests',)),
      install_requires=["nose", "mongoengine"],
      include_package_data=True,
      zip_safe=True,
      platforms=['any'],
      entry_points = {
        'nose.plugins': ['mongoengine = nose_mongoengine:MongoEnginePlugin'],
      },
)

