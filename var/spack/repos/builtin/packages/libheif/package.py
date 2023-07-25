# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libheif(CMakePackage):
    """libheif is an HEIF and AVIF file format decoder and encoder."""

    homepage = "https://github.com/strukturag/libheif"
    url = "https://github.com/strukturag/libheif/archive/refs/tags/v1.12.0.tar.gz"

    version("1.16.2", sha256="d207f2ff5c86e6af3621c237f186130b985b7a9ff657875944b58ac5d27ba71c")
    version("1.15.2", sha256="30a2736ae0247389aaa43ec70357221500c49a68db39fda94da8d5bdc786fe3b")
    version("1.14.2", sha256="e9c88e75e3b7fad9df32e42d28646752de2679df57efddfb3f63cd25110ce9d9")
    version("1.13.0", sha256="50def171af4bc8991211d6027f3cee4200a86bbe60fddb537799205bf216ddca")
    version("1.12.0", sha256="086145b0d990182a033b0011caadb1b642da84f39ab83aa66d005610650b3c65")

    depends_on("cmake@3.13:", type="build")
