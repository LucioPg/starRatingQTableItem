from setuptools import setup, find_packages

setup(
    name='starRatingQTableItem',
    version='0.1.0',
    description='A QTableItem which uses startRating delegate as default',
    url='https://github.com/LucioPG/starRatingQTableItem',
    author='LucioPg',
    author_email='',
    license='BSD 2-clause',
    install_requires=['PyQt5==5.15.6',
                      'PyQt5-Qt5==5.15.2',
                      'PyQt5-sip==12.9.0 ',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3.9',
    ],
    package_dir={"": "starRatingQTableItem"},
    packages=find_packages(where="starRatingQTableItem"),
    python_requires=">=3.6",
)
