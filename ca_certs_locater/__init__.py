# ca_certs_locater is a plug-in for httplib2 that asks it to use the 
# certificate authority file(s) from the base OS rather than the httplib2
# package. Failing to find the OS-specific file, the httplib2 file will
# be used.
#
# Copyright (c) 2013 Dan Nielsen (dnielsen@reachmail.com) 
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import ctypes.util
import collections

from ctypes import c_char_p, create_string_buffer, CDLL

try:
    libcrypto = CDLL(ctypes.util.find_library("crypto"))
except:
    raise RuntimeError("Could not find libcrypto. Do you have openssl?")

DefaultCAPaths = collections.namedtuple("DefaultCAPaths",
        "ca_file ca_path")

def _get_ssl_env_vars():

    # Set-up buffers to catch the output from the libcrypto function calls
    ca_file = create_string_buffer(75)
    ca_path = create_string_buffer(75)

    # Set return types for the libcrypto function calls
    libcrypto.X509_get_default_cert_file.restype = c_char_p
    libcrypto.X509_get_default_cert_dir.restype = c_char_p

    ca_file = libcrypto.X509_get_default_cert_file()
    ca_path = libcrypto.X509_get_default_cert_dir()

    return DefaultCAPaths(ca_file if os.path.isfile(ca_file) else None,
            ca_path if os.path.isdir(ca_path) else None)

def get():

    default_ca_vars = _get_ssl_env_vars()

    # If one of the ca_file or ca_path values has been populated by
    # by _get_ssl_env_vars, then return one of those values. ca_file
    # has priority, fall back to ca_path.
    if default_ca_vars.ca_file or default_ca_vars.ca_path:
        return default_ca_vars.ca_file or default_ca_vars.ca_path

    # Fail with an import error per the httplib2 default behavior if
    # neither a CA file or CA path has been found.
    raise ImportError()
