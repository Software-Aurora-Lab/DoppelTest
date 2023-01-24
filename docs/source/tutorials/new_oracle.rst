.. _new_oracle:

Defining Your Own Oracle
========================

In this tutorial, we will discuss how you can easily add a new oracle
into our framework.

After DoppelTest executes a scenario, each ADS instance will produce its 
own record file. In the ADS we currently focused on
(Baidu Apollo), you can either use `CyberRT Developer Tools 
<https://github.com/ApolloAuto/apollo/blob/master/docs/04_CyberRT/CyberRT_Developer_Tools.md>`_
to replay the record file and visualize it in Dreamview, or use a Python library
`cyber_record <https://github.com/daohu527/cyber_record>`_ to parse
and analyze it.

.. code-block:: bash

    root@in-dev-docker:/apollo# cyber_recorder -h
    usage: cyber_recorder -h [options]
    Unknown command: -h
    usage: cyber_recorder <command> [<args>]
    The cyber_recorder commands are:
            info    Show information of an exist record.
            play    Play an exist record.
            record  Record same topic.
            split   Split an exist record.
            recover Recover an exist record.

The record file consists messages published by each of the ADS modules
at run time. For example, messages from topic ``/apollo/planning`` corresponds
to output of the Planning module, messages from topic
``/apollo/localization/pose`` corresponds to output of the Localization module,
etc.

Consider yourself trying to implement an oracle checking if the ADS is speeding at
any point, we will call it ``SpeedingOracle``.

Step 1: What does the oracle need?
----------------------------------

The first step is to think about what the oracle does and what information does the
oracle need. To know whether the ADS is speeding, we need 2 pieces of information:
1) the ADS's current speed, 2) the speed limit of the lane which the ADS is currently
traveling in. After understanding the need of the oracle, we need to figure out what
messages from a record file should this oracle be looking at. 

Luckily, **localization messages** alone are sufficient because each of them includes 
the position and velocity of the ADS.

Step 2: Laying out the structure
--------------------------------

We have formally defined an interface for implementing a new oracle,
named :ref:`internals/framework_oracles:framework.oracles.OracleInterface`. Each new oracle should
implement 3 abstract functions defined in this interface.

.. code-block:: Python

    class SpeedingOracle(OracleInterface):
        def get_interested_topics(self):
            pass
        
        def get_results(self):
            pass
        
        def on_new_message(self, topic, message, t):
            pass

Step 3: What Topics?
--------------------

As discussed earlier, the speeding oracle only needs to know
where the ADS is and what is its speed, therefore this oracle
is only interested in messages from the localization topic.

.. code-block:: Python

    def get_interested_topics(self):
        return ['/apollo/localization/pose']


Step 4: What to do?
------------------------------------

``on_new_message`` will get called each time a new message from
the interested topic is received. The oracle should compute
the ADS's speed based on the message and check if it violated
the speed limit.

.. code-block:: Python

    def on_new_message(self, topic, message, t):
        current_speed = calculate_speed(message)
        current_position = get_position(message)

        # check which lane the ADS is currently in
        current_lane = get_current_lane(current_position)

        speed_limit = current_lane.speed_limit

        if current_speed > speed_limit:
            # a violation occurred
            pass

.. note::  Here we used some fake functions such as ``calculate_speed``,
  ``get_position``, and ``get_current_lane`` to illustrate the 
  logic behind this oracle. The complete optimized implementation
  is provided at ``framework.oracles.impl.SpeedingOracle.py``.

Step 5: What to return?
-----------------------

Now we have the first 2 parts completed, all that is left is
to produce the result. In our current implementation, the oracle
should produce a tuple describing what is the violation. Therefore
we can modify ``on_new_message`` to store that violation, so we can
return it later.

.. code-block:: Python

    def on_new_message(self, topic, message, t):
        # ......
        if current_speed > speed_limit:
            self.violation = (
                'SpeedViolation',
                f'{current_speed} violated speed limit {speed_limit}'
            )

.. code-block:: Python

    def get_result(self):
        return self.violation

.. note:: ``self.violation`` may be undefined if a violation
    never occurred. Try to implement this oracle and think
    about what to do about this!

Recap: 3 functions to define an oracle
--------------------------------------

The interface design provides an abstracted view of an obstacle: which record messages
should the oracle look at? what should the oracle do with the messages? and at the end,
what are the violations detected?
