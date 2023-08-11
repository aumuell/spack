# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NvidiaTextureTools(CMakePackage):
    """The NVIDIA Texture Tools is a collection of image processing and texture manipulation tools, designed to be integrated in game tools and asset conditioning pipelines."""

    homepage = "https://github.com/castano/nvidia-texture-tools/wiki"
    git = "https://github.com/JulianGro/nvidia-texture-tools.git"

    maintainers("aumuell")

    version("2.1.3", commit="02d38e9ea5a05383fbc276ce5949063af91f56ea")

    variant("pic", default=False, description="Produce position-independent code")
    variant("cuda", default=False, description="Use CUDA")

    depends_on("cuda@:11", when="+cuda")

    def cmake_args(self):
        spec = self.spec

        args = [
            self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
            self.define_from_variant("USE_CUDA", "cuda"),
        ]

        return args
