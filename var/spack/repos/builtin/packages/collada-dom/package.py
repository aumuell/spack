# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ColladaDom(CMakePackage):
    """COLLADA Document Object Model (DOM) C++ Library"""

    homepage = "https://www.khronos.org/collada/wiki/ColladaDOM_3"
    url = "https://github.com/rdiankov/collada-dom/archive/refs/tags/v2.5.0.tar.gz"
    git = "https://github.com/rdiankov/collada-dom.git"

    maintainers("aumuell")

    version("master", branch="master")
    version("2.5.0", sha256="3be672407a7aef60b64ce4b39704b32816b0b28f61ebffd4fbd02c8012901e0d")

    depends_on("pkgconfig", type="build")
    depends_on("boost +filesystem +system")
    depends_on("zlib-api")
    depends_on("minizip")
    depends_on("libxml2")
    depends_on("uriparser")
