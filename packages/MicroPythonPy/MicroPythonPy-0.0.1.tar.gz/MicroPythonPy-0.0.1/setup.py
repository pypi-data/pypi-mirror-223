from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'MicroPythonPy'
LONG_DESCRIPTION = 'An module for Machine learning alogirthms in micro python'

# Setting up
setup(
    name="MicroPythonPy",
    version=VERSION,
    author="Avinash",
    author_email="avi999880@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyttsx3', 'speech_recognition', 'pyautogui', 'pydirectinput', 'cv2'],
    keywords=['MicroMachinePy', 'Machine', 'micromachinepy', 'machine learning', 'ESP32'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)