""" Unit tests for pystorge """

# Copyright (C) 2021 Gwyn Ciesla

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
import getpass
import tempfile
import configparser
import datetime
from OpenSSL import crypto

import pystorge

def test_humansize():
    """ Test conversion of bytes to more human readable units """
    assert pystorge.humansize(102814) == '100.40K'

def test_homesub():
    """ Test homedir ~ substitution """
    assert pystorge.homesub('~/.pystorge.conf') == \
        os.path.expanduser('~' + getpass.getuser()) + '/.pystorge.conf'

def test_client_config_handler():
    """ Ensure that the generated client config is what we expect. """

    handle, path = tempfile.mkstemp() # pylint: disable=unused-variable
    testconf = pystorge.client_config_handler(path) # pylint: disable=unused-variable
    config = configparser.ConfigParser()
    config.read(path)
    os.unlink(path)

    assert str(config.get("Options", "url")) == 'https://127.0.0.1:8080/'
    assert str(config.get("Options", "password")) == 'storge'

def test_server_config_handler():
    """ Ensure that the generated server config is what we expect. """

    handle, path = tempfile.mkstemp() # pylint: disable=unused-variable
    testconf = pystorge.server_config_handler(path) # pylint: disable=unused-variable
    config = configparser.ConfigParser()
    config.read(path)
    os.unlink(path)

    assert str(config.get("Options", "database")) == 'storge'
    assert str(config.get("Options", "dbpass")) == 'storge'
    assert str(config.get("Options", "ip")) == '127.0.0.1'
    assert str(config.get("Options", "port")) == '8080'
    assert str(config.get("Options", "dbhost")) == '127.0.0.1'
    assert str(config.get("Options", "password")) == 'storge'
    assert str(config.get("Options", "key")) == '~/.storge_key.pem'
    assert str(config.get("Options", "cert")) == '~/.storge_cert.pem'
    assert str(config.get("Options", "title")) == 'Storge'

def test_create_certs():
    """ Test that we're creating valid key/certificate pairs. """
    khandle, kpath = tempfile.mkstemp() # pylint: disable=unused-variable
    os.unlink(kpath)
    chandle, cpath = tempfile.mkstemp() # pylint: disable=unused-variable
    os.unlink(cpath)

    status = pystorge.create_certs(kpath, cpath)

    assert status == 0

    with open(kpath, 'r', encoding='utf-8') as keyfile:
        keycontent = keyfile.read()
    key = crypto.load_privatekey(crypto.FILETYPE_PEM, keycontent)
    assert isinstance(key, crypto.PKey) is True

    os.unlink(kpath)
    os.unlink(cpath)

def test_cert_expiry():
    """ Make sure we can obtain certificate expiration dates, and that they're for a year. """

    khandle, kpath = tempfile.mkstemp() # pylint: disable=unused-variable
    os.unlink(kpath)
    chandle, cpath = tempfile.mkstemp() # pylint: disable=unused-variable
    os.unlink(cpath)

    status = pystorge.create_certs(kpath, cpath)

    assert status == 0

    expdate = pystorge.cert_expiry(cpath)
    parsed = datetime.datetime.strptime(expdate, '%Y-%m-%d %H:%M:%S')
    assert isinstance(parsed, datetime.datetime)
    assert parsed - datetime.datetime.today() > datetime.timedelta(days=364)

    os.unlink(kpath)
    os.unlink(cpath)
