import xbmcgui, xbmc, xbmcaddon
import sys, os, time, platform

# Script constants:
__scriptname__ = "Mount TrueCrypt"
__author__ = "Douglas Orend"
__version__ = "2.1"

# Required addon variables:
addon = xbmcaddon.Addon(id='script.mount.truecrypt')
txt = addon.getLocalizedString

############################################################################
def mount_container(tc, dir="", pwd="", key="", hidden=False):
	# Figure out what the parameters should be:
	if key == "":
		key = '""'
	if hidden == False:
		hidden = 'no'
	else:
		hidden = 'yes'

	# Retrieve password and error out if blank:
	if pwd == "":
		pwd = xbmcgui.Dialog().input(txt(32000), option=xbmcgui.ALPHANUM_HIDE_INPUT)
	if pwd == "":
		xbmcgui.Dialog().ok(txt(32003), txt(32009))
		return

	# Attempt to mount the container:
	if os.system(executable + ' --text --non-interactive --mount -p ' + pwd + ' -k ' + key + ' --protect-hidden=' + hidden + ' ' + tc + ' ' + dir) == 0:
		xbmcgui.Dialog().ok(txt(32001), txt(32002))
	else:
		xbmcgui.Dialog().ok(txt(32003), txt(32004))

############################################################################
def unmount_container(tc, unmount=False):
	if not unmount:
		unmount = is_mounted(tc) and xbmcgui.Dialog().yesno(txt(32010), txt(32011), nolabel=txt(32012))
	if unmount:
		if os.system(executable + ' --text --non-interactive -d -f ' + tc) == 0:
			xbmcgui.Dialog().ok(txt(32005), txt(32006))
		else:
			xbmcgui.Dialog().ok(txt(32007), txt(32008))

############################################################################
def is_mounted(tc):
	return os.system(executable + ' --text --non-interactive --list ' + tc) == 0

############################################################################
def get_params():
	param=[]
	try:
		paramstring=sys.argv[2]
	except:
		return {}
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param

############################################################################
# Get the addon settings:
executable   = addon.getSetting("executable").decode('utf-8')
container    = addon.getSetting("container").decode('utf-8')
mountdir     = addon.getSetting("mountdir").decode('utf-8')

# Error out if this addon is being run on Windows:
if platform.system() == "Windows":
	xbmcgui.Dialog().ok(txt(31000), txt(31001))

# Are the settings okay to work with?
elif not os.path.exists(executable):
	if xbmcgui.Dialog().yesno(txt(31002), txt(31003), txt(31010)):
		addon.openSettings()
elif not os.path.exists(container):
	if xbmcgui.Dialog().yesno(txt(31004), txt(31005), txt(31010)):
		addon.openSettings()
elif mountdir == "":
	if xbmcgui.Dialog().yesno(txt(31006), txt(31007), txt(31010)):
		addon.openSettings()
elif not os.path.exists(mountdir):
	if xbmcgui.Dialog().yesno(txt(31008), txt(31009), txt(31010)):
		addon.openSettings()

# Okay, settings are okay!  Let's do this!
else:
	# Get the parameters being passed.  If "force" parameter is passed, unmount without prompting!
	params = get_params()
	try:
		forced = params['force'] != ''
	except:
		forced = False

	# If forced parameter specified or is mounted, then unmount the container!
	if forced or is_mounted(container):
		unmount_container(tc=container, unmount=forced)
	# Otherwise, try and mount the container!
	else:
		mount_container(tc=container, dir=mountdir)
