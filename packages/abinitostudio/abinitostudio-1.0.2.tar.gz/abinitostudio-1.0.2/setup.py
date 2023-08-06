from setuptools import setup

setup(name="abinitostudio",
    version="1.0.2",
    description="A studio for first-principles calculations.",
    long_description="This is a long description.",
    author="Pan Zhou, Xin Lu and Li Zhongsun",
    author_email="zhoupan71234@xtu.edu.cn",
    classifiers=["Development Status :: 3 - Alpha",'Programming Language :: Python',],
    packages=['abinitostudio',
			  'abinitostudio.calculation',
              'abinitostudio.io', 
              'abinitostudio.plot', 
              'abinitostudio.structure', 
              'abinitostudio.ui',],
    scripts=[
        "scripts/cal_vasp_single.py",
    ],
	include_package_data = True,
	package_data={
        "abinitostudio.images": ["imagges/*"],
        "abinitostudio.doc": ["doc/*"],
        'abinitostudio.examples': ['examples/*'],
    },
    install_requires=[
		'paramiko==2.7.1',
		'jumpssh==1.6.5',
		'numpy==1.18.3',
		'pyxtal==0.3.0',
		'ase==3.19.1',
		'pymatgen==2020.4.2',
		'vtk==8.1.2',
		'pyface==6.1.2',
		'traits==6.0.0',
		'traitsui==7.0.0',
		'PyQt5==5.11.2',
		'envisage==4.9.2',
		'mayavi==4.7.1',
    ],
	python_requires=">=3.7, <=3.12", #add the restriction for now issue 
    license="MIT",

)
