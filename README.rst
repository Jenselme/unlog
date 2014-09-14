Unlog
=====

The purpose of this software is to help you filter logs when you need to view
more than the line containing the error pattern. The advantage of ``unlog``
versus ``grep`` with the ``-A`` or ``-B`` options is that ``unlog`` only print
the lines you need no matter how much of them they are.

For instance, with the following example:

::

   /home/assos/drupal7/sites/assos.centrale-marseille.fr.accueil
   Cron run successful.                                                 [success]
   /home/assos/drupal7/sites/assos.centrale-marseille.fr.jenselmetest
   Command core-cron needs a higher bootstrap level to run - you will   [error]
   need to invoke drush from a more functional Drupal environment to run
   this command.
   /home/assos/drupal7/sites/assos.centrale-marseille.fr.jenselme
   Cron run successful.

We only want to get the group of lines containing the error and its
description. So in this case, if the above lines where on stdin ``|
unlog --error-pattern error --start-pattern
/home/assos/drupal7/sites/assos.centrale-marseille.fr.\w+`` would output:

::

   /home/assos/drupal7/sites/assos.centrale-marseille.fr.jenselmetest
   Command core-cron needs a higher bootstrap level to run - you will   [error]
   need to invoke drush from a more functional Drupal environment to run
   this command


Configuration file
==================

You can use a configuration file. By default, unlog will look for
``~/.unlog``. With the ``--config`` option you can select your own.

The section names must be the name of the file you want to process. You can use
the ``~`` character to represent home or any glob like ``*`` in the section
name.

If you want to use a config file while processing the standard input, you must
specify which section to use with the ``--use-config-section`` argument.


Example
-------

.. code:: ini

	  [TEST]
	  start pattern = /home/assos/drupal7/sites/assos.centrale-marseille.fr.\w
	  error pattern = (error|warning)

	  [~/*/unlog/test/program_output_config]
	  # The left argument of an include directive must be an exact section title
	  # Any new option here will override those in the included section.
	  include	= TEST

	  [~/*/unlog/test/program_output_mail]
	  start pattern = /home/assos/drupal7/sites/assos.centrale-marseille.fr.\w
	  error pattern = (error|warning)
	  mail from = unlog@jujens.eu
	  mail to = jenselme@ec-m.fr
	  mail subject = Pytest unlog


Group
=====

If the log has group (eg by command or by date), unlog can group the
output. Simply provide a ``start group pattern`` (or ``--start-group``) and a
``end group pattern`` (or ``--end-group``) in your config file (or in the
command line).

Example
-------

With the following log:

::

   %%%% Drush cron — 2014-09-15
   /home/assos/drupal7/sites/assos.centrale-marseille.fr.jenselmetest
   Cron run successful.                                                 [1;32;40m[1m[success][0m
   /home/assos/drupal7/sites/assos.centrale-marseille.fr.jenselme
   WD php: PDOException: SQLSTATE[HY000] [2002] Operation timed out in  [31;40m[1m[error][0m
   drupal_is_denied() (line 1916 of
   /home/assos/drupal7/includes/bootstrap.inc).
   PDOException: SQLSTATE[HY000] [2002] Operation timed out in drupal_is_denied() (line 1916 of /home/assos/drupal7/includes/bootstrap.inc).
   Drush command terminated abnormally due to an unrecoverable error.   [31;40m[1m[error][0m
   /home/assos/drupal7/sites/assos.centrale-marseille.fr.jenselmetest2
   Cron run successful.                                                 [1;32;40m[1m[success][0m
   %%%% END

and this config:

.. code:: ini

	  [TEST]
	  start pattern = /home/assos/drupal7/sites/assos.centrale-marseille.fr.\w
	  error pattern = (error|warning)

	  [~/*/unlog/test/program_output_group]
	  include = TEST
	  start group pattern = %%%% (?P<command>\w+) — (?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})
	  end group pattern = %%%% END

You get this output:

::

   GROUP: Drush cron — 2014-09-15
   /home/assos/drupal7/sites/assos.centrale-marseille.fr.jenselme
   WD php: PDOException: SQLSTATE[HY000] [2002] Operation timed out in  [31;40m[1m[error][0m
   drupal_is_denied() (line 1916 of
   /home/assos/drupal7/includes/bootstrap.inc).
   END GROUP: Drush cron — 2014-09-15

You are not compelled to use the ``?P<command>`` and ``?P<date>``. If they are
present, their content will be printed on the ``GROUP:`` line. Otherwise,
nothing will be printed.
