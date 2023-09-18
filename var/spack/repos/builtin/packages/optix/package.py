# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform
import subprocess
import sys

from spack.package import *


class Optix(Package):
    """NVIDIA OptiX Ray Tracing Engine"""

    homepage = "https://developer.nvidia.com/rtx/ray-tracing/optix"
    url = "https://developer.nvidia.com/downloads/designworks/optix/secure/8.0.0/nvidia-optix-sdk-8.0.0-linux64-x86_64.sh"

    maintainers("aumuell")

    manual_download = True

    conflicts("platform=darwin")
    if platform.machine() not in ["aarch64", "arm64", "x86_64"]:
        conflicts("platform=linux")

    if platform.machine() in ["aarch64", "arm64"]:
        version("8.0.0", sha256="05e47b8617db5fffdb7417914255fd395c16d39c83ec71084864b47178de640b", expand=False)
        version("7.7.0", sha256="05ee7b8617db5fffdb7417914255fd395c16d39c83ec71084c64b47178de640b", expand=False)
        version("7.5.0", sha256="05ee7b8617db5fffdb7417914255fd395c16d39c83ec71084e64b47178de640b", expand=False)

    if platform.machine() in ["x86_64"]:
        version("8.0.0", sha256="81308cf525a3034c8059c6ce805bd63e57e91a31d50dd336757c6d59c9fbfaf0", expand=False)
        version("7.7.0", sha256="c558c51235afe859847681e96f1950600dcd10ba96791bc1e059e19730602a9c", expand=False)
        version("7.6.0", sha256="05e47ba617db5fffdb7417914255fd395c16d39c83ec71084864b471d8d76e0b", expand=False)
        version("7.5.0", sha256="ec8f80350870275e6536a4150a65976d7b391f605ef2c09616486569aa60b670", expand=False)

    variant("accept-eula", default=False, description="Accept the EULA")

    depends_on("cuda", type="build")
    # "recommended" CUDA versions, but others should work, too
    #depends_on("cuda@12.0", when="@8.0", type="build")
    #depends_on("cuda@12.0", when="@7.7", type="build")
    #depends_on("cuda@11.8", when="@7.6", type="build")
    #depends_on("cuda@11.7", when="@7.5", type="build")

    @staticmethod
    def installer_for_version(version):
        ver = version.dotted
        if platform.machine() in ["aarch64", "arm64"]:
            return "NVIDIA-OptiX-SDK-{0}-linux64-aarch64.sh".format(ver)
        if platform.machine() in ["x86_64"]:
            if ver == "7.6.0":
                return "NVIDIA-OptiX-SDK-{0}-linux64-x86_64-31894579.sh".format(ver)
            return "NVIDIA-OptiX-SDK-{0}-linux64-x86_64.sh".format(ver)

    def url_for_version(self, version):
        cwd = os.getcwd()
        file = self.installer_for_version(version)
        return "file://{0}/{1}".format(cwd, file)

    def install(self, spec, prefix):
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
        installer = self.installer_for_version(spec.version)
        #subprocess.run(["/bin/sh", installer], input=b"y\nn\n") # accept license, don't include package name into extraction directory
        subprocess.run(["/bin/sh", installer, "--exclude-subdir", "--skip-license"])

        # copy to installation prefix
        install_tree("include", prefix.include)
