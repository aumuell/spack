# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

from spack.pkg.builtin.opencover import Opencover


class Covise(Opencover):
    """Collaborative Visualization and Simulation Environment"""

    homepage = "https://www.hlrs.de/covise"
    git      = "https://github.com/hlrs-vis/covise.git"

    maintainers = ['aumuell']

    # FIXME: Add proper versions and checksums here.
    # version('1.2.3', '0123456789abcdef0123456789abcdef')
    version('master', branch='master', submodules=True)

    provides('cover')

    variant('vtk', default=False, description='Read VTK data')
    variant('assimp', default=False, description='Read polygonal models in various formats')
    variant('netcdf', default=False, description='Read WRFChem and other NetCDF based data formats')

    depends_on('git', type='build')
    depends_on('cmake@3.3:', type='build')

    depends_on('python@2.7:', type=('build', 'run'))

    depends_on('netcdf-cxx4', when='+netcdf')

    #depends_on('tbb')

    depends_on('libzip')
    depends_on('libarchive')

    depends_on('cgns')
    depends_on('vtk', when='+vtk')

    depends_on('assimp', when='+assimp')
    depends_on('hdf5', when='+hdf5')

    depends_on('libmicrohttpd')
    #depends_on('coin3d')
    #depends_on('openssl')
    depends_on('gdal')
    depends_on('libgeotiff')
    depends_on('proj@:8.99')

    def cmake_args(self):
        """Populate cmake arguments for COVISE."""

        args = Opencover.cmake_covise_args(self)

        return args
