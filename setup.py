import os, setuptools
dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, 'requirements.txt')) as f:
    required_packages = f.read().splitlines()
with open(os.path.join(dir_path, 'README.md'), "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='cucopy',
    version='1.0',
    author='Julian Schönau, Patrick Kuckertz, Jann Weinand, Leander Kotzur, Detlef Stolten',
    author_email='j.schoenau@fz-juelich.de, p.kuckertz@fz-juelich.de, j.weinand@fz-juelich.de, l.kotzur@fz-juelich.de, d.stolten@fz-juelich.de',
    description='Module for exchanging monetary values and inflation adjustment.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://jugit.fz-juelich.de/iek-3/groups/data-and-model-integration/cucopy',
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=required_packages,
    setup_requires=['setuptools-git'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    keywords=['money', 'finance', 'inflation'],
)