from setuptools import setup, find_packages

setup(
    name="tf_datachain",
    version="0.1.0",
    description="A local dataset loader based on tf.data input pipeline",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Yiming Liu",
    author_email="YimingDesigner@gmail.com",
    package_dir={'':"src"},
    packages=find_packages("src"),
    install_requires=[
        "numpy",
        "matplotlib",
        "pandas",
        "tensorflow",
        "keras-cv",
        "keras-core",
        "opencv-python",
    ],
)