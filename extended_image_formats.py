from nodes import SaveImage
import json
from PIL import Image
import folder_paths
import numpy as np
from PIL.PngImagePlugin import PngInfo
import os
from comfy.cli_args import args


avif_supported = False
jxl_supported = False

# Avif
try:
    import pillow_avif  # noqa: F401
except:  # noqa: E722
    pass
else:
    avif_supported = True

# Jxl
try:
    from jxlpy import JXLImagePlugin  # noqa: F401
except:  # noqa: E722
    pass
else:
    jxl_supported = True


class ExtendedSaveImage(SaveImage):
    @classmethod
    def INPUT_TYPES(s):
        output = {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
                "format": (["png", "jpeg", "webp"],),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

        if avif_supported:
            output["required"]["format"][0].append("avif")
        if jxl_supported:
            output["required"]["format"][0].append("jxl")

        return output

    RETURN_TYPES = ()

    FUNCTION = "save_images"

    CATEGORY = "image"

    def save_images(
        self,
        images,
        filename_prefix="ComfyUI",
        format="png",
        prompt=None,
        extra_pnginfo=None,
    ):
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = (
            folder_paths.get_save_image_path(
                filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0]
            )
        )
        results = list()
        for batch_number, image in enumerate(images):
            i = 255.0 * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            metadata = None
            if not args.disable_metadata:
                metadata = PngInfo()
                if prompt is not None:
                    metadata.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo is not None:
                    for x in extra_pnginfo:
                        metadata.add_text(x, json.dumps(extra_pnginfo[x]))

            filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_.{format}"

            if format == "png":
                img.save(
                    os.path.join(full_output_folder, file),
                    pnginfo=metadata,
                    compress_level=self.compress_level,
                )

            else:
                if format == "jxl":
                    print("JXL export doesn't have metadata/import support yet!")

                exif = {}

                if prompt is not None:
                    exif["prompt"] = prompt
                if extra_pnginfo is not None:
                    for info in extra_pnginfo:
                        exif[info] = extra_pnginfo[info]

                if extra_pnginfo["workflow"]:
                    imgexif = img.getexif()
                    imgexif[0x9286] = json.dumps(exif)  # UserComment

                img.save(os.path.join(full_output_folder, file), exif=imgexif)

            results.append(
                {"filename": file, "subfolder": subfolder, "type": self.type}
            )
            counter += 1

        return {"ui": {"images": results}}
