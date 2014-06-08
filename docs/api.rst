.. _api:

API
===

.. module:: plan

This part covers some interfaces of Plan.


Plan Object
-----------

.. autoclass:: Plan
   :members:


Job Objects
-----------

.. autoclass:: Job
   :members:

.. autoclass:: CommandJob
   :members:

   .. attribute:: cron

       The cron syntax content of this job object.

.. autoclass:: ScriptJob
   :members:

.. autoclass:: ModuleJob
   :members:
