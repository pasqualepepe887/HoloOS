from gradio_client import Client, file
import sys
import os

path_img = sys.argv[1]


client = Client("TencentARC/InstantMesh")
result = client.predict(
		input_image=file(path_img),
		api_name="/check_input_image"
)

result = client.predict(
		input_image=file(path_img),
		do_remove_background=True,
		api_name="/preprocess"
)

result = client.predict(
		input_image=file(path_img),
		sample_steps=75,
		sample_seed=42,
		api_name="/generate_mvs"
)

result = client.predict(
		api_name="/make3d"
)
print(result)

#os.popen('python3 3drender.py ' + result[0])

os.popen('python3 3drender.py ' + result[0])


