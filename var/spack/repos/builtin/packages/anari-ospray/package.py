# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AnariOspray(CMakePackage):
    """Translation layer from ANARI to OSPRay, ANARILibrary and ANARIDevice "ospray"."""

    homepage = "https://github.com/ospray/anari-ospray"
    git = "https://github.com/ospray/anari-ospray.git"

    maintainers("aumuell")

    version("main", branch="main")

    depends_on("ospray@2.12:")
    depends_on("anari-sdk@0.4:")
    depends_on("python@3")
