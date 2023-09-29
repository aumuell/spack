# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Minizip(AutotoolsPackage):
    """C library for zip/unzip via zLib."""

    homepage = "https://www.winimage.com/zLibDll/minizip.html"
    url = "https://zlib.net/fossils/zlib-1.2.11.tar.gz"

    version("1.3", sha256="ff0ba4c292013dbc27530b3a81e1f9a813cd39de01ca5e0f8bf355702efa593e")
    version("1.2.13", sha256="b3a24de97a8fdbc835b9833169501030b8977031bcb54b3b3ac13740f846ab30")
    version("1.2.12", sha256="91844808532e5ce316b3c010929493c0244f3d37593afd6de04f71821d5136d9")

    version("1.2.11", sha256="c3e5e9fdd5004dcb542feda5ee4f0ff0744628baf8ed2dd5d66f8ca1197cb1a1")

    configure_directory = "contrib/minizip"

    depends_on("automake", type="build")
    depends_on("autoconf", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("zlib-api")

    # error: implicit declaration of function 'mkdir' is invalid in C99
    patch("implicit.patch", when="@:1.2.11 %apple-clang@12:")
    patch("implicit.patch", when="@:1.2.11 %gcc@7.3.0:")

    # statically link to libz.a
    # https://github.com/Homebrew/homebrew-core/blob/master/Formula/minizip.rb
    patch("static.patch", when="%apple-clang@12:")

    # build minizip and miniunz
    @run_before("autoreconf")
    def build_minizip_binary(self):
        configure()
        make()
        with working_dir(self.configure_directory):
            make()

    # install minizip and miniunz
    @run_after("install")
    def install_minizip_binary(self):
        mkdirp(self.prefix.bin)
        with working_dir(self.configure_directory):
            install("minizip", self.prefix.bin)
            install("miniunz", self.prefix.bin)
