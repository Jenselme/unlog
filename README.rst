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
