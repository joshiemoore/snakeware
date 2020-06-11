################################################################################
#
# python-pygame-gui
#
################################################################################

PYTHON_PYGAME_GUI_VERSION = 0.5.6
PYTHON_PYGAME_GUI_SOURCE = pygame_gui-$(PYTHON_PYGAME_GUI_VERSION).tar.gz
PYTHON_PYGAME_GUI_SITE = https://files.pythonhosted.org/packages/b9/13/02b9e546e072497b510f9fd4480e420bba0da8e7999a8fc5e5daa2aa70bd
PYTHON_PYGAME_GUI_SETUP_TYPE = setuptools
PYTHON_PYGAME_GUI_LICENSE = MIT

$(eval $(python-package))
