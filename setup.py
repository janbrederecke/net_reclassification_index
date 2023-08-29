from setuptools import find_packages, setup

setup(
    name="net_reclassification_index",
    packages=find_packages(where="net_reclassification_index"),
    package_dir={"": "net_reclassification_index"},
    version="0.1.0",
    description="Net Reclassification Index for survival data.",
    author="Jan Brederecke",
    license="MIT",
    setup_requires=[
        "numpy",
        "pandas",
        "scipy",
    ],
)
