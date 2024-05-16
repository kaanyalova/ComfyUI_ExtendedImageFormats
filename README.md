# Extended Image Formats for ComfyUI


Adds a custom node for saving images in webp, jpeg, avif, jxl (no metadata)

Metadata is saved in UserComment(0x9286) field of Images,

Its formatted as 
```
{
    "prompt": { Prompt data... }
    "workflow": { Workflow data... }
    "some_extra_pnginfo_field": {...}
}

```



## Installation
Clone the repo inside your `custom_nodes` folder
```
git clone https://github.com/kaanyalova/ComfyUI_ExtendedImageFormats
```

For avif support install `pillow-avif-plugin`, for jxl support install `jxlpy` to your venv
```
source ./venv/bin/activate
pip install pillow-avif-plugin jxlpy
```