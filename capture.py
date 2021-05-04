# import standard modules
from PIL import Image
import time
import os
import sys
import glob
import ctypes
import site
use_imageio = False
if sys.version >= 3.0:
	try:
		import imageio
		use_imageio = True
	except ImportError:
		pass
else:
	print('imageio not used. Using PIL gif generator instead.')

# import maya modules
from maya import cmds
from maya import OpenMayaUI
from maya import OpenMaya
import shiboken2
from PySide2 import QtWidgets

# import custom modules
import grabimage

# define custom variables
ctypes.windll.user32.SetProcessDPIAware()  # for DPI scaling
dir_path = os.path.dirname(os.path.realpath(__file__))
output_path = dir_path + "/output"
pil_path = "C:/Python27/Lib/site-packages/PIL"
site.addsitedir('C:/Python27/Lib/site-packages')


def do_it():
	create_dir()
	if not os.path.exists("output/"):
		os.mkdir("output")
	for fname in glob.glob("output/*.bmp"):
		os.remove(fname)
	capture_screen_position(numShots=20, delaySec=1/5)
#	if use_imageio:
#		imageio_convert_img_to_gif()
#	else:
#		pil_convert_img_to_gif()


def get_main_window():
	"""
	Get the main Maya window as a QtGui.QMainWindow instance
	:returns: QtGui.QMainWindow instance of the top level Maya windows
	"""
	ptr = OpenMayaUI.MQtUtil.mainWindow()
	if ptr is not None:
		return shiboken2.wrapInstance(long(ptr), QtWidgets.QWidget)


def get_window_bbox():
	"""
	returns a window bbox
	:return:
	"""
	width, height = get_model_editor_screen_port()
	window = get_main_window()
	bbox = window.geometry()
	x = bbox.x()
	y = bbox.y()
	# if x <= 0:
		# width = 0
	return x, y, width, height


def create_int_ptr():
	u_util = OpenMaya.MScriptUtil()
	int_ptr = u_util.asIntPtr()
	return int_ptr


def get_int_from_int_ptr(int_ptr):
	u_util = OpenMaya.MScriptUtil()
	float_val = u_util.getInt(int_ptr)
	return float_val


def create_dir():
	"""creates directory"""
	print('output_dir: {}'.format(output_path))
	if not os.path.exists(output_path):
		os.mkdir(output_path)


def imageio_convert_img_to_gif():
	"""images to gif"""
	images = []
	filenames = os.listdir(output_path)
	for filename in filenames:
		images.append(imageio.imread(output_path + '/' + filename))
	imageio.mimsave(output_path + '/movie.gif', images)


def pil_convert_img_to_gif():
	"""pillow image capture"""
	fp_in = output_path + '/.png'
	fp_out = output_path + "/image.gif"
	imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
	# img.save(fp=fp_out, format='GIF', append_images=imgs, save_all=True, duration=200, loop=0)


def capture_screen_position(numShots=1, delaySec=0):
	"""capture and save screenshot(s)"""
	for n in range(numShots):
		bbox = get_window_bbox()
		im = grabimage.grab_screen(bbox=bbox)
		fname = output_path + "/%.02f.bmp" % time.time()
		print("saving [%s] (%d of %d)" % (fname, n + 1, numShots))
		im.save(fname)
		if delaySec:
			time.sleep(delaySec)


def get_model_editor_screen_position():
	"""
	returns the model editor screen position
	:return:
	"""
	model_editor = 'modelPanel4'
	x = create_int_ptr()
	y = create_int_ptr()
	view = OpenMayaUI.M3dView()
	OpenMayaUI.M3dView.getM3dViewFromModelEditor(model_editor, view)
	view.getScreenPosition(x, y)
	view_x = get_int_from_int_ptr(x)
	view_y = get_int_from_int_ptr(y)
	return view_x, view_y


def get_model_editor_screen_port():
	"""
	returns the model editor screen position
	:return: <>
	"""
	model_editor = 'modelPanel4'
	view = OpenMayaUI.M3dView()
	OpenMayaUI.M3dView.getM3dViewFromModelEditor(model_editor, view)
	view_y = view.portHeight()
	view_x = view.portWidth()
	return view_x, view_y


def get_panel_in_focus():
	focus_panel_name = cmds.getPanel(withFocus=True)
	return focus_panel_name


def get_panel_under_cursor():
	cursor_panel_name = cmds.getPanel(underPointer=True)
	return cursor_panel_name


if __name__ == "__main__":
	do_it()

# ______________________________________________________________________________________________________________________
# go3.py
