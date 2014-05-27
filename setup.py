"""
Plan
----

Cron jobs in Python.

Links
`````

* `documentation <https://github.com/fengsp/plan>`_
* `development version
  <http://github.com/fengsp/plan/zipball/master#egg=plan-dev>`_

"""
from setuptools import setup


setup(
    name='plan',
    version='0.1',
    url='https://github.com/fengsp/plan',
    license='BSD',
    author='Shipeng Feng',
    author_email='fsp261@gmail.com',
    description='A Python package for writing and deploying cron jobs '
                'with a clear and beautiful syntax.',
    long_description=__doc__,
    packages=['plan'],
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
    ],
)
