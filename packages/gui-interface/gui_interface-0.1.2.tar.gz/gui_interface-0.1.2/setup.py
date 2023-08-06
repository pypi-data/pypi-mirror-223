from setuptools import setup, find_packages

setup(
    name='gui_interface',
    version='0.1.2',
    packages=find_packages(),
    author='Daniel Hahaj',
    author_email='dhahaj@gmail.com',
    description='A short description of my package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dhahaj/gui_interface',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[
        "bcrypt==4.0.1",
        "colorama==0.4.6",
        "loguru==0.7.0",
        "markdown-it-py==3.0.0",
        "mdurl==0.1.2",
        "Pygments==2.15.1",
        "pyserial==3.5",
        "PySide6==6.5.2",
        "PySide6-Addons==6.5.2",
        "PySide6-Essentials==6.5.2",
        "rich==13.5.2",
        "shiboken6==6.5.2",
        "telemetrix==1.20",
        "win32-setctime==1.1.0",
    ],
    entry_points={
        'console_scripts': ['gui_interface=gui_interface.main:main']
    },
)

# from setuptools import setup

# setup(
#     name="GuiInterface",
#     version="0.1",
#     packages=["gui_interface"],
#     install_requires=[
#         "bcrypt==4.0.1",
#         "colorama==0.4.6",
#         "loguru==0.7.0",
#         "markdown-it-py==3.0.0",
#         "mdurl==0.1.2",
#         "Pygments==2.15.1",
#         "pyserial==3.5",
#         "PySide6==6.5.2",
#         "PySide6-Addons==6.5.2",
#         "PySide6-Essentials==6.5.2",
#         "rich==13.5.2",
#         "shiboken6==6.5.2",
#         "telemetrix==1.20",
#         "win32-setctime==1.1.0",
#     ],
# )
