################################################################################
#
# python-pyttsx3
#
################################################################################

PYTHON_PYTTSX3_VERSION = 2.87
PYTHON_PYTTSX3_SOURCE = v$(PYTHON_PYTTSX3_VERSION).tar.gz
PYTHON_PYTTSX3_SITE = https://github.com/nateshmbhat/pyttsx3/archive
PYTHON_PYTTSX3_SETUP_TYPE = setuptools
PYTHON_PYTTSX3_LICENSE = GPL-3.0

$(eval $(python-package))
