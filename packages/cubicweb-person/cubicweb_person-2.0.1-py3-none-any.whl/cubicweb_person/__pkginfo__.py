# pylint: disable-msg=W0622
"""cubicweb-person packaging information"""

modname = 'person'
distname = "cubicweb-%s" % modname

numversion = (2, 0, 1)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
description = "person component for the CubicWeb framework"
author = "Logilab"
author_email = "contact@logilab.fr"
web = 'https://www.cubicweb.org/project/%s' % distname
classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
    ]

__depends__ = {
    'cubicweb': '>=4.0.0,<5.0.0',
    'cubicweb-web': '>= 1.0.0,<2.0.0'
}
__recommends__ = {'cubicweb-addressbook': None}
