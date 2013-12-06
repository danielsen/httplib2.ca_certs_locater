ca_certs_locater is a plug-in for httplib2 that asks it to use the 
certificate authority file(s) from the base OS rather than the httplib2
package. Failing to find he OS-specific file, the httplib2 file will
be used.

Installation
============
::
  $ python setup.py install

Cautions
========
::
  Currently, this module is linux only
