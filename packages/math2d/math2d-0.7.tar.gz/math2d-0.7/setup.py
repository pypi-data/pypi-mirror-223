from distutils.core import setup
from distutils.command.install_data import install_data

setup (
    name='math2d',
    version='0.7',
    description='2D mathematics package for Python.',
    author='Morten Lind',
    author_email='morten@lind.fairuse.org',
    url='https://codeberg.org/moli/pymath2d',
    packages=['math2d', 'math2d.geometry'],
    provides=['math2d'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
    ],
    license='GNU Lesser General Public License v3 (LGPLv3)',
    data_files=[('share/doc/pymath2d', ['COPYING'])]
)
