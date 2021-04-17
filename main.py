from Photobooth import TkinterApp
import os

# Create a folder to save photos to
folder = r"/photos/"
cwd = os.getcwd()
path = cwd + folder
if not os.path.exists(path):
    os.makedirs(path)
# Run application
app = TkinterApp()
app.mainloop()
