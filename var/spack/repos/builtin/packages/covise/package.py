# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Covise(CMakePackage):
    """Collaborative Visualization and Simulation Environment"""

    homepage = "https://www.hlrs.de/covise"
    git      = "https://github.com/hlrs-vis/covise.git"

    maintainers = ['aumuell']

    # FIXME: Add proper versions and checksums here.
    # version('1.2.3', '0123456789abcdef0123456789abcdef')
    version('develop', branch='master', submodules=True)

    depends_on('python@2.7:2.8', when='+python2', type=('build', 'run'))
    depends_on('python@3:', when='+python', type=('build', 'run'))

    depends_on('flex', type='build')
    depends_on('bison', type='build')
    depends_on('swig', type='build')

    depends_on('xerces-c')
    depends_on('curl')
    depends_on('qt+opengl')
    depends_on('glu')
    depends_on('glew')
    depends_on('mpi')
    depends_on('boost+pic')

    # depends_on('netcdf-cxx4', when='+netcdf')
    depends_on('cmake@3.3:', type='build')

    depends_on('tbb')

    depends_on('zlib')
    depends_on('libzip')

    depends_on('cfitsio')
    depends_on('cgns')
    #depends_on('vtk')

    depends_on('ffmpeg')
    #depends_on('embree')
    depends_on('libtiff')
    depends_on('libpng')
    depends_on('zlib')
    depends_on('libjpeg-turbo')
    depends_on('assimp')
    depends_on('hdf5')

    depends_on('libmicrohttpd')
    #depends_on('openssl')
    depends_on('gdal')
    depends_on('proj')
    depends_on('speex')

    # depends_on('vtk', when='+vtk')

    # depends_on('assimp', when='+assimp')

    # depends_on('openscenegraph', when='+osg')
    depends_on('openscenegraph')

    def cmake_args(self):
        """Populate cmake arguments for COVISE."""

        spec = self.spec

        args = []

        args.append('-DCOVISE_WARNING_IS_ERROR=OFF')
        args.append('-DCOVISE_USE_VISIONARAY=OFF')
        args.append('-DCOVISE_USE_CUDA:BOOL=OFF')
        args.append('-DCOVISE_CPU_ARCH:STRING=')

        return args
