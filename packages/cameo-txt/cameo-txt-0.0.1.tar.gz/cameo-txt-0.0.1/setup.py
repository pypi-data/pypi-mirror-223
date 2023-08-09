from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cameo-txt',
    version='0.0.1',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'requests==2.28.2',
        'python-docx==0.8.11',
        'PyPDF2==3.0.1',
        'chardet==3.0.4',
        'odfpy==1.4.1',
    ],
    author='JcXGTcW',
    description='將各種格式的檔案提取成txt',
)
