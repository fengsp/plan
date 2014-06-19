"""
Plan
----

Cron jobs in Python.

Plan is easy
````````````

Save in a schedule.py:

.. code:: python
    
    from plan import Plan

    cron = Plan()

    cron.command('ls /tmp', every='1.day', at='12:00')
    cron.command('pwd', every='2.month')
    cron.command('date', every='weekend')

    if __name__ == "__main__":
        cron.run()

And run it:

.. code:: bash

    $ pip install plan
    $ python schedule.py

Links
`````

* `github <https://github.com/fengsp/plan>`_
* `development version
  <http://github.com/fengsp/plan/zipball/master#egg=plan-dev>`_

"""
from setuptools import setup


setup(
    name='plan',
    version='0.2',
    url='https://github.com/fengsp/plan',
    license='BSD',
    author='Shipeng Feng',
    author_email='fsp261@gmail.com',
    description='A Python package for writing and deploying cron jobs '
                'with a clear and beautiful syntax.',
    long_description=__doc__,
    packages=['plan', 'plan.testsuite'],
    entry_points={
        'console_scripts': [
            'plan-quickstart = plan.commands:quickstart'
        ]
    },
    install_requires=[
        'click==2.1'
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
