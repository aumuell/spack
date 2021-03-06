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
    version('2019.9', tag='v2019.9', submodules=True)
    version('2020.1', tag='v2020.1', submodules=True)
    version('2020.2', commit='3efd1e7718d30718a6f7c0cddc3999928dc02a9d', submodules=True)
    version('2020.8', commit='aaf99ff79145c10a6ba4754963266244b1481660', submodules=True)
    version('2020.9', tag='v2020.9', submodules=True)

    variant('rr', default=True, description='Enable remote rendering')
    variant('python', default=True, description='Enable Python support')
    variant('qt', default=False, description='Build graphical workflow editor relying ond Qt')
    variant('vtk', default=False, description='Enable reading VTK data')
    variant('netcdf', default=False, description='Enable reading of WRF data')
    variant('osg', default=False, description='Build renderer relying on OpenSceneGraph')
    variant('vr', default=False, description='Build virtual environment render module based on OpenCOVER')
    variant('assimp', default=False, description='Enable reading of polygonal models (.obj, .stl, ...)')
    variant('proj', default=False, description='Enable MapDrape module for carthographic coordinate mappings')

    variant('static', default=False, description='Do not build shared libraries')
    variant('multi', default=False, description='Use a process per module')
    variant('double', default=False, description='Use double precision scalars')
    variant('large', default=False, description='Use 64-bit indices')

    conflicts('%gcc@:4.99')

    extends('python', when='+python')

    depends_on('python@2.7:', when='+python', type=('build', 'run'))

    depends_on('mpi')
    depends_on('botan')
    depends_on('boost@1.59:')
    depends_on('boost+pic')

    depends_on('netcdf-cxx', when='+netcdf')
    #if spec.satisfies('^netcdf-cxx'):
    #    depends_on('netcdf-cxx')
    depends_on('cmake@3.3:', type='build')

    depends_on('tbb')

    depends_on('zstd')
    depends_on('lz4')
    depends_on('snappy')

    depends_on('zlib')
    depends_on('libzip')
    #depends_on('libarchive')

    depends_on('vtk', when='+vtk')
    depends_on('tinyxml2', when='+vtk')

    depends_on('assimp', when='+assimp')
    #if spec.satisfies('^assimp'):
    #    depends_on('assimp')
    depends_on('proj', when='+proj')

    depends_on('openscenegraph@3.4:', when='+osg')
    depends_on('glew', when='+osg')
    depends_on('glu', when='+osg')
    #if spec.satisfies('^openscenegraph@3.4:') \
    #        and spec.satisfies('^glew') \
    #        and spec.satisfies('^glu'):
    #    depends_on('openscenegraph@3.4:')

    depends_on('jpeg', when='+rr')
    depends_on('embree+ispc', when='+rr')
    depends_on('ispc', when='+rr', type='build')

    depends_on('cover@2020.11:', when='+vr')

    def cmake_args(self):
        """Populate cmake arguments for Vistle."""
        spec = self.spec

        args = []

        args.append('-DVISTLE_PEDANTIC_ERRORS=OFF')
        args.append('-DCOVISE_ARCHSUFFIX=spack')

        if '+python' in spec:
            if spec.satisfies('^python@:2.99'):
                args.extend([
                    '-DVISTLE_USE_PYTHON2=ON'
                ])
            else:
                args.extend([
                    '-DVISTLE_USE_PYTHON2=OFF'
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
