# BNotebooks

A Blender add-on that enables the use of Blender as a kernel for Jupyter Notebooks.

This is a repackaging of [`blender_notebook`](https://github.com/cheng-chi/blender_notebook), but as an installable Blender add-on. Packaging it as an add-on removes the need for another python environment for installation, and keeps Blender's bundled python environment more isolated for better reproducibility.

## Installation
Install the `addon.zip` via the `Addons` tab in the `Preferences`.

`Blender Prefernces` -> `Add-ons` -> `Install` 

Select the `BNotebooks_X.zip`. Click the top left tick box to enable the addon, which will display the add-on preferences. Click the `Install ipykernel` button to install the required package, then click `Append Kernel` to register this Blender as a kernel for use in Jupyter Notebooks.

![](https://i.imgur.com/FcB230V.png)

### This Blender version will now be available as a jupyter kernel.
