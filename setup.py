import setuptools


classifiers = [
    (
        'Programming Language :: Python :: %s' % x
    )
    for x in '3.6 3.7 3.8'.split()
]


setuptools.setup(
    name='maxfucktor',
    description='Brainfuck to ASM translator',
    version='0.1.0',
    license='MIT license',
    platforms=['unix', 'linux'],
    keywords=['brainfuck', 'asm', 'compiler'],
    author='magniff',
    url='https://github.com/magniff/maxfucktor',
    classifiers=classifiers,
    packages=setuptools.find_packages(),
    install_requires=[
        'funcparserlib', 'click', 'Jinja2'
    ],
    entry_points={
        'console_scripts': [
            'bfcompiler=bin.bfcompiler:main',
            'pprinter=bin.pprinter:main',
        ]
    },
    zip_safe=False,
)

