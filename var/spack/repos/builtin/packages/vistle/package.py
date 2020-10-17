# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Vistle(CMakePackage):
    """Vistle is a tool for visualization of scientific data in VR.

    Notable features are distributed workflows and low-latency remote
    visualization."""

    homepage = 'https://www.vistle.io'
    git      = "https://github.com/vistle/vistle.git"

    maintainers = ['aumuell']

    version('develop', branch='master', submodules=True)
    # version('2020.02', commit='3efd1e7718d30718a6f7c0cddc3999928dc02a9d', submodules=True)
    # version('2020.08', commit='aaf99ff79145c10a6ba4754963266244b1481660', submodules=True)

    variant('rr', default=True, description='Enable remote rendering')
    variant('python2', default=False, description='Enable Python2 support')
    variant('python', default=True, description='Enable Python(3) support')
    variant('qt', default=False, description='Enable Qt (gui) support')
    variant('vtk', default=False, description='Enable reading VTK data')
    variant('netcdf', default=False, description='Enable reading of WRF data')
    variant('osg', default=False, description='Build renderer relying on OpenSceneGraph')
    variant('vr', default=False, description='Build virtual environment render module based on OpenCOVER')
    variant('assimp', default=False, description='Enable reading of polygonal models (.obj, .stl, ...)')

    variant('static', default=False, description='Do not build shared libraries')
    variant('multi', default=False, description='Use a process per module')
    variant('double', default=False, description='Use double precision scalars')
    variant('large', default=False, description='Use 64-bit indices')

    conflicts('+python', when='+python2')
    conflicts('%gcc@:4.99')

    extends('python', when='+python2')
    extends('python', when='+python')

    depends_on('python@2.7:2.8', when='+python2', type=('build', 'run'))
    depends_on('python@3:', when='+python', type=('build', 'run'))

    depends_on('mpi')
    depends_on('botan')
    depends_on('boost+pic')

    depends_on('netcdf-cxx4', when='+netcdf')
    depends_on('cmake@3.3:', type='build')

    depends_on('tbb')

    depends_on('zstd')
    depends_on('lz4')
    depends_on('snappy')

    depends_on('zlib')
    depends_on('libzip')
    depends_on('libarchive')

    depends_on('vtk', when='+vtk')
    depends_on('tinyxml2', when='+vtk')

    depends_on('assimp', when='+assimp')
    depends_on('proj')

    depends_on('openscenegraph', when='+osg')
    depends_on('glew', when='+osg')
    depends_on('glu', when='+osg')

    depends_on('jpeg', when='+rr')
    depends_on('embree+ispc', when='+rr')
    depends_on('ispc', when='+rr', type='build')

    depends_on('covise', when='+vr')

    def cmake_args(self):
        """Populate cmake arguments for Vistle."""
        spec = self.spec

        args = []

        args.append('-DVISTLE_PEDANTIC_ERRORS=OFF')

        if '+python' in spec:
            args.extend([
                '-DVISTLE_USE_PYTHON3=ON'
            ])
        if '+python2' in spec:
            args.extend([
                '-DVISTLE_USE_PYTHON3=OFF'
            ])
        if '+multi' in spec:
            args.append('-DVISTLE_MULTI_PROCESS=ON')
        else:
            args.append('-DVISTLE_MULTI_PROCESS=OFF')

        if '+static' in spec:
            args.extend([
                '-DVISTLE_BUILD_SHARED=OFF',
                '-DVISTLE_MODULES_SHARED=OFF'
            ])

        if '+double' in spec:
            args.append('-DVISTLE_DOUBLE_PRECISION=ON')
        else:
            args.append('-DVISTLE_DOUBLE_PRECISION=OFF')

        if '+large' in spec:
            args.append('-DVISTLE_64BIT_INDICES=ON')
        else:
            args.append('-DVISTLE_64BIT_INDICES=OFF')

        return args
