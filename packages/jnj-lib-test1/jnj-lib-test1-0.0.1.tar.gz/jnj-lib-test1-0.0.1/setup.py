from setuptools import setup

setup(
    name="jnj-lib-test1",
    version="0.0.1",
    description="PYPI test package",
    author="moondevpy",
    author_email="moondevpy@gmail.com",
    url="https://github.com/moondevpy/jnj_lib",
    install_requires=["pyyaml"],
    packages=["jnj_lib_base", "jnj-lib-doc"],
    # packages=find_packages(exclude=[]),
    keywords=["jnj test", "pypi test"],
    python_requires=">=3.11",
    # package_data={},
    # zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3.11",
    ],
)
