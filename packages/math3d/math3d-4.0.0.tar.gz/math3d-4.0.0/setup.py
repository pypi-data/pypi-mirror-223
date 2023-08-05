from setuptools import setup

setup(
    name='math3d',
    version='4.0.0',
    description='3D Special Euclidean mathematics package for Python.',
    author='Morten Lind',
    author_email='morten@lind.fairuse.org',
    url='https://codeberg.org/moli/pymath3d',
    packages=['math3d', 'math3d.interpolation', 'math3d.reference_system',
              'math3d.dynamics', 'math3d.geometry', 'math3d.visualization'],
    provides=['math3d'],
    install_requires=['numpy', 'matplotlib'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
    ],
    license='GNU Lesser General Public License v3 (LGPLv3)',
    data_files=[('share/doc/pymath3d', ['README.md', 'COPYING.LESSER'])]
)
