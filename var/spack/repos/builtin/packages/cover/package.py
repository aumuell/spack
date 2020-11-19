# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

from sys import platform

class Cover(CMakePackage):
    """Collaborative Visualization and Simulation Environment"""

    homepage = "https://www.hlrs.de/opencover"
    git      = "https://github.com/hlrs-vis/covise.git"

    maintainers = ['aumuell']

    # FIXME: Add proper versions and checksums here.
    # version('1.2.3', '0123456789abcdef0123456789abcdef')
    version('develop', branch='master', submodules=True)

    variant('x11', default=not platform=='darwin', description='Use X11 Window system')
    variant('mpi', default=False, description='Enable MPI support - required for Vistle')
    variant('embree', default=False, description='Interactive spray simulation')
    variant('virvo', default=True, description='Enable volume rendering')
    variant('visionaray', default=False, description='Enable interactive ray-tracing')

    depends_on('cmake@3.3:', type='build')

    depends_on('python@2.7:', type=('build', 'run'))

    depends_on('flex', type='build')
    depends_on('bison', type='build')
    depends_on('swig', type='build')

    depends_on('xerces-c')
    depends_on('curl')
    depends_on('qt+opengl')
    depends_on('glu')
    depends_on('glew')
    depends_on('openscenegraph')
    depends_on('libx11', when='+x11')

    depends_on('mpi', when='+mpi')

    depends_on('boost')
    #depends_on('tbb', when='+virvo')

    #depends_on('cfitsio', when='+virvo')

    depends_on('ffmpeg')
    depends_on('embree', when='+embree')

    depends_on('zlib')
    depends_on('libpng')
    depends_on('libtiff')
    depends_on('libjpeg-turbo')

    #depends_on('speex')

    package_spec = {
        'cfitsio': 'cfitsio',
        'Boost': 'boost',
        'OPENSSL': 'openssl',
        'OpenSSL': 'openssl',
        'Git': 'git',
        'VTK': 'vtk',
        'JPEGTURBO': 'libjpeg-turbo',
        'JPEG': 'jpeg',
        'FFMPEG': 'ffmpeg',
        'FFMPEG_SWSCALE': 'ffmpeg',
        'SNAPPY': 'snappy',
        'TBB': 'tbb',
        'MPI': 'mpi',
        'FLEX': 'flex',
        'BISON': 'bison',
        'SWIG': 'swig',
        'embree': 'embree',
        'SPEEX': 'speex',
        'PROJ4': 'proj',
        'SDL': 'sdl2',
        'EIGEN': 'eigen',
        'GDAL': 'gdal',
        'GeoTIFF': 'libgeotiff',
        'VTKm': 'vtk-m',
        'Freeimage': 'freeimage',
        'BLAS': 'blas',
        'LAPACK': 'lapack',
        'Cg': None,
        'HIDAPI': None,
        'Alut': None,
        'OpenVR': None,
        'PCL': None,
        'PythonLibs': 'python',
        'LibUSB1': 'libusb',
        'X11': 'libx11',
        'OpenCV': 'opencv',
        'GLUT': 'freeglut',
        'LibVncServer': None,
        'NVML': None,
        'VRPN': None,
        'Steereo': None,
        'FMOD': None,
        'WiringPi': None,
        'ARToolKit': None,
        'NATNET': None,
        'ZSPACE': None,
        'OSGCAL': None,
        'OsgQt': None,
        'OsgEarth': None,
        'Faro': None,
        'JT': None,
        'SISL': None,
        'E57': None,
        'OVR': None,
        'OsgEphemeris': None,
        'SLAM6D': None,
        'WiiYourself': None,
        'PHYSX': None,
        'CUDPP': None,
        'JSBSim': None,
        'OpenCRG': None,
        'LAMURE': None,
        'Schism': None,
        'MidiFile': None,
        'OSC': None,
        'WMFSDK': None,
        'Surface': None,
        'OpenEXR': 'openexr',
        'CUDA': 'cuda',
        'PbrtParser': None,
        'Bonjour': None,
        'VolPack': None,
        'Nifti': None,
        'NORM': None,
        'Protokit': None,
        'Teem': None,
        'GDCM': None,
        #'PTHREAD': None,
    }

    def cmake_args(self):
        """Populate cmake arguments for COVISE."""

        spec = self.spec

        args = [
            self.define_from_variant('COVISE_USE_VIRVO', 'virvo'),
            self.define_from_variant('COVISE_USE_VISIONARAY', 'visionaray'),
            self.define_from_variant('COVISE_USE_X11', 'x11'),
        ]

        args.append('-DCOVISE_WARNING_IS_ERROR=OFF')
        args.append('-DCOVISE_BUILD_ONLY_COVER=ON')

        args.append('-DCOVISE_CPU_ARCH:STRING=')
        args.append('-DARCHSUFFIX:STRING=spack')

        for package in self.package_spec:
            s = self.package_spec[package]
            if not s or not spec.satisfies('^'+s):
                args.append('-DCMAKE_DISABLE_FIND_PACKAGE_'+package+'=TRUE')

        return args
