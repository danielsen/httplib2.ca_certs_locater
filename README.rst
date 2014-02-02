ca_certs_locater
================
ca_certs_locater is a plug-in for httplib2 that asks it to use the 
certificate authority file(s) from the base OS rather than the httplib2
package. Failing to find he OS-specific file, the httplib2 file will
be used.

Installation
============
  $ python setup.py install

Usage
=====
There is no need to include this plug-in directly in your Python program.
After installation it will be automatically used by httplib2 to locate 
system certificate authority files.

However, if you do want to include it or use it, do the following:
  >>> import ca_certs_locater
  >>> ca_file = ca_certs_locater.get()

Cautions
========
Currently, this module is linux only
