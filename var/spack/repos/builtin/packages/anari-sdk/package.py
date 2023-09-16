# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AnariSdk(CMakePackage):
    """ANARI SDK"""

    homepage = "https://registry.khronos.org/ANARI/"
    url = "https://github.com/KhronosGroup/ANARI-SDK/archive/refs/tags/v0.7.2.tar.gz"
    git = "https://github.com/KhronosGroup/ANARI-SDK.git"

    maintainers("aumuell")

    version("main", branch="main")
    version("0.7.2", sha256="98972e5936f7c8a93cc4d4b60be096b90b0de7c3398c2f4f530b20b7724b3f1d")
    version("0.3.0", sha256="917621a0a28ffad1ad652c647268f73ab67e7dec1b9cd71c5f20be74b5a55b8b")
    version("0.2.0", sha256="e81a0f2dd6cf61d55a23815b26f610777cfcba2026836bbad2778a15f8d0e9e7")
    version("0.1.2", sha256="b99e687b3167125ab515e3311a11fe6eb3190e404814eff0c30202372c57e07f")

    variant("shared", default=True, description="Build shared libraries")
    variant("viewer", default=False, description="Build viewer application")
    variant("examples", default=False, description="Build example applications")
    variant("helide", default=False, description="Build helide device (using Embree)")
    variant("remote", default=False, description="Build remote device")

    depends_on("glfw", when="+viewer")
    depends_on("embree@4", when="+helide")

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = []
        args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))
        args.append(self.define_from_variant("BUILD_HELIDE_DEVICE", "helide"))
        args.append(self.define_from_variant("BUILD_REMOTE_DEVICE", "remote"))
        args.append(self.define_from_variant("BUILD_EXAMPLES", "examples"))
        args.append(self.define_from_variant("BUILD_VIEWER", "viewer"))
        return args
