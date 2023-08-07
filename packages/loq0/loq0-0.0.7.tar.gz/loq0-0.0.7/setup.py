import setuptools

install_requires = [
    'numpy==1.25.2'
]

setuptools.setup(
    name="loq0",
    version="0.0.7",
    author="seorii",
    author_email="me@seorii.page",
    description="League of Quoridor",
    long_description="League of Quoridor",
    long_description_content_type="text/markdown",
    url="https://github.com/dastyinc/loq0",
    packages=[
        'loq0',
        'loq0.state',
        'loq0.state.validate',
        'loq0.state.actions',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

)
