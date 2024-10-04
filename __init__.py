from .extended_image_formats import ExtendedSaveImage, DDSSaveImage


# Set the web directory, any .js file in that directory will be loaded by the frontend as a frontend extension
WEB_DIRECTORY = "./web/"

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {"ExtendedSaveImage": ExtendedSaveImage, "DDSSaveImage": DDSSaveImage}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {"ExtendedSaveImage": "Extended Save", "DDSSaveImage": "Save DDS for games"}
