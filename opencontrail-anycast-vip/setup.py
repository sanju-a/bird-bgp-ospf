#
# Copyright (c) 2015 Juniper Networks, Inc.
#

import setuptools


def requirements(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines

setuptools.setup(
    name='opencontrail-anycast-vip',
    version='0.3.5',
    packages=setuptools.find_packages(),

    # metadata
    author="OpenContrail",
    author_email="dev@lists.opencontrail.org",
    license="Apache Software License",
    url="http://www.opencontrail.org/",
    description="OpenContrail anycast vip",
    long_description="This module checks for HAProxy's health and confiures anycast VIP",

    install_requires=requirements('requirements.txt'),

    test_suite='opencontrail_anycast_vip.tests',
    tests_require=requirements('test-requirements.txt'),

    entry_points = {
        'console_scripts': [
            'opencontrail-anycast-vip = opencontrail_anycast_vip:main',
        ],
    },
)
