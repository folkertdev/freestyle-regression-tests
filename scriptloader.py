import sys
import os
import bpy
import importlib.machinery

"""
This file imports the correct style module. This makes sure the most recent version of the style module is used. 
(reason for this is that otherwise after every edit to a style module it had to be reloaded in blender, which is a pain.)
"""
blend_dir = os.path.dirname(bpy.data.filepath)
style_module_name = bpy.data.filepath.split("\\")[-1].split(".")[0] + "_style_module.py"

loader = importlib.machinery.SourceFileLoader(style_module_name, os.path.join(blend_dir, style_module_name))
style_module = loader.load_module()




