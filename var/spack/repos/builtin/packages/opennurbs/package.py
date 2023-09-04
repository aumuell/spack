# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Opennurbs(CMakePackage, MakefilePackage):
    """OpenNURBS is an open-source NURBS-based geometric modeling library
    and toolset, with meshing and display / output functions.
    """

    homepage = "https://opennurbs.org"
    git = "https://github.com/mcneel/opennurbs.git"

    maintainers("jrood-nrel")

    version("develop", git="https://github.com/OpenNURBS/OpenNURBS.git", branch="develop")

    version("8.x", branch="8.x")
    version("7.x", branch="7.x", preferred=True)
    version("6.x", branch="6.x")

    version(
        "percept",
        sha256="d12a8f14f0b27d286fb7a75ab3c4e300f77d1fbb028326d1c8d28e4641605538",
        url="https://github.com/PerceptTools/percept/raw/master/build-cmake/opennurbs-percept.tar.gz",
    )

    build_system(
        conditional("makefile", when="@:7"), conditional("cmake", when="@8:"), default="cmake"
    )
    variant("shared", default=True, when="build_system=cmake", description="Build shared libraries")


    def cmake_args(self):
        spec = self.spec
        args = std_cmake_args

        args.extend([self.define_from_variant("BUILD_SHARED_LIBS", "shared")])

        return args

    # Pre-cmake installation method
    @when("@:7")
    def install(self, spec, prefix):
        make(parallel=False)

        # Install manually
        mkdir(prefix.lib)
        mkdir(prefix.include)
        if self.spec.satisfies("@6:"):
            install("libopennurbs_public.a", prefix.lib)
        else:
            install("libopenNURBS.a", prefix.lib)
        install_tree("zlib", join_path(prefix.include, "zlib"))
        install("*.h", prefix.include)
