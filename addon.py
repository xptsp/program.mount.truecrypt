import xbmcgui, xbmc, xbmcaddon
import sys, os, time, platform

# Script constants:
__scriptname__ = "Mount TrueCrypt"
__author__ = "Douglas Orend"
__version__ = "1.0"

# Required addon variables:
__addon__ = xbmcaddon.Addon(id='script.mount.truecrypt')
__localizedMessages__ = __addon__.getLocalizedString


def get_password(pwd = ""):
	if pwd == "":
		return xbmcgui.Dialog().input(__localizedMessages__(32000), option=xbmcgui.ALPHANUM_HIDE_INPUT)
	else:
		return pwd


def mount_container(tc, dir="", pwd="", key="", hidden=False):
	# Figure out what the parameters should be:
	if key == "":
		key = '""'
	if hidden == False:
		hidden = 'no'
	else:
		hidden = 'yes'

	# Retrieve password and error out if blank:
	password = get_password(pwd)
	if password == "":
		xbmcgui.Dialog().ok(__localizedMessages__(32003), __localizedMessages__(32009))
		return

	# Attempt to mount the container:
	if os.system(executable + ' --text --non-interactive --mount -p ' + password + ' -k ' + key + ' --protect-hidden=' + hidden + ' ' + tc + ' ' + dir) == 0:
		xbmcgui.Dialog().ok(__localizedMessages__(32001), __localizedMessages__(32002))
	else:
		xbmcgui.Dialog().ok(__localizedMessages__(32003), __localizedMessages__(32004))


def unmount_container(tc):
	if os.system(executable + ' --text --non-interactive -d ' + tc) == 0:
		xbmcgui.Dialog().ok(__localizedMessages__(32005), __localizedMessages__(32006))
	else:
		xbmcgui.Dialog().ok(__localizedMessages__(32007), __localizedMessages__(32008))


def is_mounted(tc):
	return os.system(executable + ' --text --non-interactive --list ' + tc) == 0


# Get the addon settings:
executable   = __addon__.getSetting("executable").decode('utf-8')
container    = __addon__.getSetting("container").decode('utf-8')
mountdir     = __addon__.getSetting("mountdir").decode('utf-8')

# Error out if this addon is being run on Windows:
if platform.system() == "Windows":
	xbmcgui.Dialog().ok(__localizedMessages__(31000), __localizedMessages__(31001))

# Are the settings okay to work with?
elif not os.path.exists(executable):
	xbmcgui.Dialog().ok(__localizedMessages__(31002), __localizedMessages__(31003))
elif not os.path.exists(container):
	xbmcgui.Dialog().ok(__localizedMessages__(31004), __localizedMessages__(31005))
elif mountdir == "":
	xbmcgui.Dialog().ok(__localizedMessages__(31006), __localizedMessages__(31007))
elif not os.path.exists(mountdir):
	xbmcgui.Dialog().ok(__localizedMessages__(31008), __localizedMessages__(31009))

# Okay, settings are okay!  Let's do this!
else:
	if not is_mounted(container):
		mount_container(container, mountdir)
	else:
		unmount_container(container)
