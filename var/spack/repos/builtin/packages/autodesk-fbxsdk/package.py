# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import subprocess
import sys

from spack.package import *


class AutodeskFbxsdk(Package):
    """Autodesk FBX Software Developer Kit"""

    homepage = "https://www.autodesk.com/developer-network/platform-technologies/fbx"
    url = "https://www.autodesk.com/content/dam/autodesk/www/adn/fbx/2020-3-4/fbx202034_fbxsdk_linux.tar.gz"

    maintainers("aumuell")

    manual_download = True

    if sys.platform == "linux":
        version("2020.3.4", sha256="05e47b8617db5fffdb7417914255fd395c16d39c83ec71084864b47178d7640b")
    if sys.platform == "darwin":
        version("2020.3.4", sha256="a01168ed54d798aa477a9345b3b9c0332c964d5ae3fd306a238974ccfd017bb1")

    variant("accept-eula", default=False, description="Accept the EULA")
    variant("debug", default=False, description="Install debug instead of release libraries")

    def url_for_version(self, version):
        ver = version.joined
        cwd = os.getcwd()
        if sys.platform == "linux":
            return "file://{0}/fbx{1}_fbxsdk_linux.tar.gz".format(cwd, ver)
        if sys.platform == "darwin":
            return "file://{0}/fbx{1}_fbxsdk_clang_mac.pkg.tgz".format(cwd, ver)

    def install(self, spec, prefix):
        # check compatibility
        if sys.platform != "darwin" and sys.platform != "linux":
            raise InstallError(
                "\n\nOnly compatible with linux and darwin platforms"
            )
        elif sys.platform == "linux" and not spec.satisfies("target=x86_64:"):
            raise InstallError(
                "\n\nOnly compatible with linux on x86_64"
            )

        # check license acceptance
        if not self.spec.variants["accept-eula"].value:
            install_example = "spack install autodesk-fbxsdk +accept-eula"
            raise InstallError(
                "\n\nNOTE: Use +accept-eula "
                + "during installation "
                + "to accept the license terms in:\n"
                + "  {0}\n".format(join_path(self.stage.source_path, tmplic))
                + "Example: '{0}'".format(install_example)
            )

        # extract from downloaded archive
        ver = spec.version
        debrel = "debug" if spec.satisfies("+debug") else "release"
        if sys.platform == "darwin":
            subprocess.call(["pkgutil", "--expand-full", "fbx{0}_fbxsdk_clang_macos.pkg".format(ver.joined), "expanded/"])
            tmplic = join_path("expanded", "Root.pkg", "Payload", "Applications", "Autodesk", "FBX SDK", ver.dotted, "License.rtf")
            tmpinc = join_path("expanded", "Root.pkg", "Payload", "Applications", "Autodesk", "FBX SDK", ver.dotted, "include")
            tmplib = join_path("expanded", "Root.pkg", "Payload", "Applications", "Autodesk", "FBX SDK", ver.dotted, "lib", "clang", debrel)
        elif sys.platform == "linux":
            installer = "./fbx{0}_fbxsdk_linux".format(ver.joined)
            os.chmod(installer, 0o755)
            mkdirp("expanded/")
            subprocess.run([installer, "expanded/"], input=b"yes\nn\n") # accept license and do not show readme
            tmplic = join_path("expanded", "License.txt")
            tmpinc = join_path("expanded", "include")
            tmplib = join_path("expanded", "lib", "gcc", "x64", debrel)

        # copy to installation prefix
        install(tmplic, prefix)
        install_tree(tmpinc, prefix.include)
        install_tree(tmplib, prefix.lib)
