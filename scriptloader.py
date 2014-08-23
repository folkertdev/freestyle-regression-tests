import sys
import os
import bpy
import importlib.machinery


blend_dir = os.path.dirname(bpy.data.filepath)
style_module_name = bpy.data.filepath.split("\\")[-1].split(".")[0] + "_style_module.py"



loader = importlib.machinery.SourceFileLoader(style_module_name, os.path.join(blend_dir, style_module_name))
style_module = loader.load_module()




