# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Visrtx(CMakePackage):
    """NVIDIA RTX based implementation of ANARI
    VisRTX is an experimental, scientific visualization-focused implementation of the Khronos ANARI standard, and is developed by the HPC Visualization Developer Technology team at NVIDIA."""

    homepage = "https://www.example.com"
    url = "https://github.com/NVIDIA/VisRTX/archive/refs/tags/v0.6.1.tar.gz"
    git = "https://github.com/NVIDIA/VisRTX.git"

    maintainers("aumuell")

    version("0.6.1", sha256="70ec9730f2c30007b2c810b788d1a7f36021a83f0aa44d050ad0f6ea71558718")
    version("0.5.0", sha256="4310e05e9a794d5809653227c598330bc9ed0aaa64b2dee494e531061f6b3135")
    version("0.4.0", sha256="a0d82a64ff6471a551d1f3bfbc493cc8cac5b714f1467571192f5eef48a08361")

    variant("optix", default=False, description="Build VisRTX raytracing backend using NVIDIA Optix")
    variant("gl", default=False, description="Build VisGL backend using OpenGL 3")

    requires("platform=linux", when="+optix", msg="current versions of OptiX do not work on macOS")
    requires("platform=linux", when="+gl", msg="CMake does not provide OpenGL::OpenGL on macOS")
    # does not make sense to build neither of the two backends
    conflicts("~gl", when="~optix", msg="at least one backend should be built")

    depends_on("cmake@3.17:")
    depends_on("cuda@11.3.1:", when="+optix")
    depends_on("optix@7.4:", when="+optix")
    depends_on("gl@3:", when="+gl")
    depends_on("anari-sdk@0.7:")
    #C++17 compiler
    #NVIDIA Driver 495+

    def cmake_args(self):
        args = [
            self.define_from_variant("VISRTX_BUILD_RTX_DEVICE", "optix"),
            self.define_from_variant("VISRTX_BUILD_GL_DEVICE", "gl"),
        ]
        return args
