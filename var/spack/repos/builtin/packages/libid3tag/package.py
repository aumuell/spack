# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *


class Libid3tag(CMakePackage, AutotoolsPackage):
    """library for id3 tagging"""

    homepage = "https://www.underbit.com/products/mad/"
    url = "https://codeberg.org/tenacityteam/libid3tag/archive/0.16.2.tar.gz"

    maintainers("TheQueasle")

    version("0.16.2", sha256="02721346d554c4b4aa3966b134152be65eb4df1fb9322d2d019133238d2ba017")
    version("0.15.1b", sha256="63da4f6e7997278f8a3fef4c6a372d342f705051d1eeb6a46a86b03610e26151")

    depends_on("zlib-api")
    depends_on("gperf")

    # source: https://git.archlinux.org/svntogit/packages.git/tree/trunk/10_utf16.diff?h=packages/libid3tag
    patch("10_utf16.diff", when="@0.15")
    # source: https://git.archlinux.org/svntogit/packages.git/tree/trunk/11_unknown_encoding.diff?h=packages/libid3tag
    patch("11_unknown_encoding.dif", when="@0.15")
    # source: https://git.archlinux.org/svntogit/packages.git/tree/trunk/CVE-2008-2109.patch?h=packages/libid3tag
    patch("CVE-2008-2109.patch", level=0, when="@0.15")
    # source: https://git.archlinux.org/svntogit/packages.git/tree/trunk/libid3tag-gperf.patch?h=packages/libid3tag
    patch("libid3tag-gperf.patch", when="@0.15 ^gperf@3.1:")

    # Build system
    build_system(
        conditional("cmake", when="@0.16:"), conditional("autotools", when="@:0.15"), default="cmake"
    )

    with when("build_system=cmake"):
        generator("ninja")
        depends_on("cmake@3.9:", type="build")

    with when("build_system=autotools"):
        depends_on("gmake", type="build")

    @run_before("configure")
    def preclean(self):
        """
        Remove compat.c and frametype.c in order to regenerate from gperf
        sources
        """
        os.remove("compat.c")
        os.remove("frametype.c")
