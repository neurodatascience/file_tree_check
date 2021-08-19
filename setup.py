from setuptools import setup, find_packages

setup(
    name='file_tree_check',
    packages=find_packages("src"),
    package_dir={"": "src"},
    url='https://github.com/btoutee/file_tree_check',
    license='LICENSE.txt',
    author='Bertrand Toutée',
    author_email='bertrand.toutee@gmail.com',
    description='File checking script in a repeating folder organization e.g. BIDS.',
    python_requires=">=3.6"
)
