"""
    create an animated gif from the Maya viewport
"""
# import standard modules
from PIL import Image
import os
import glob
import site

# import maya modules
from maya import cmds

# define custom variables
dir_path = os.path.dirname(os.path.realpath(__file__))
output_path = dir_path + "/output"
pil_path = "C:/Python27/Lib/site-packages/PIL"
site.addsitedir('C:/Python27/Lib/site-packages')
extension_name = 'jpg'
duration = 50


def do_it():
    """capture"""
    create_dir()
    remove_files()
    capture_viewport()


def remove_files():
    """
    remove the frames before and after gif creation
    :return: <bool> True for success
    """
    for fname in glob.glob(output_path + "/*.{}".format(extension_name)):
        os.remove(fname)
    return True


def get_anim_timeline_min_max():
    """
    return minimum time, maximum time
    :return: <float> min time, <float> max time
    """
    min_time = cmds.playbackOptions(q=True, minTime=True)
    max_time = cmds.playbackOptions(q=True, maxTime=True)
    return min_time, max_time


def get_anim_keyframe_min_max():
    """
    get the min max keyframe values
    :return: <float>, <float> min, max keyframe
    """
    anims = cmds.ls(type='animCurve')
    frames = sorted(cmds.keyframe(anims, q=1))
    min_frame = frames[0]
    max_frame = frames[len(frames)-1]
    return min_frame, max_frame


def capture_viewport():
    """
    capture the information from the viewport
    :return: <bool> True for success
    """
    min_frame, max_frame = get_anim_keyframe_min_max()
    create_dir()
    for frame in range(int(min_frame), int(max_frame)):
        cmds.playblast(fr=frame, v=False, fmt="image", c=extension_name, orn=False,
                       cf=output_path + '/screen_capture_{}.{}'.format(frame, extension_name), p=100)
    pil_convert_img_to_gif()
    remove_files()
    return True


def create_dir():
    """
    creates directory
    :return: <str> output path
    """
    print('output_dir: {}'.format(output_path))
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    return output_path


def pil_convert_img_to_gif():
    """
    pillow image capture
    :return: <bool> True for success
    """
    fp_in = output_path + '/*.' + extension_name
    fp_out = output_path + "/image.gif"
    imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
    img = imgs[0]
    img.save(fp=fp_out, format='GIF', append_images=imgs, save_all=True, duration=duration, loop=0)
    return True

# ______________________________________________________________________________________________________________________
# animgif.py
