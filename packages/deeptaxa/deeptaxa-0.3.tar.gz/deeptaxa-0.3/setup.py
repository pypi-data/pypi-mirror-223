from setuptools import setup, find_packages

setup(
    name='deeptaxa',
    version='0.3',
    description='DeepTaxa is a deep learning tool for taxonomic classification of bacterial genomes',
    #long_description=open('README.md').read(),
    author='Yuguo Zha, Haobo Zhang, Kang Ning',
    author_email='hugozha@hust.edu.cn, ningkang@hust.edu.cn',
    maintainer='Yuguo Zha',
    maintainer_email='hugozha@hust.edu.cn',
    license='GPL-3.0 License',
    platforms=["linux"],
    url='https://github.com/HUST-NingKang-Lab/DeepTaxa',
    packages=find_packages(),
    #entry_points={
    #    'console_scripts': ['data = DeepTaxa.script.data', 'predict = DeepTaxa.script.predict']
    #},
    scripts=['DeepTaxa/data.py', 'DeepTaxa/predict.py', 'DeepTaxa/script/hmmer.sh', 'DeepTaxa/script/mmseqs.sh'],
    include_package_data=True,
    package_data={
        'DeepTaxa': ['data/*','config/*','genomes/*','script/*']
    },
    classifiers=[
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3'
)
