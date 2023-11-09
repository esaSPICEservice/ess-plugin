import os
import glob

LOCAL_PATH = 'LOCAL_PATH'

def create_local_metakernel(base_dir):
    templates = os.path.join(base_dir, '..', 'kernels', 'mk', '*')
    target_dir = os.path.join(base_dir, '..', 'kernels')
    local_kernel_path = os.path.abspath(target_dir)

    kernels = [item for item in  glob.glob(templates)]

    for kernel in kernels:
        new_filename = os.path.join(target_dir, os.path.basename(kernel) + '.local')
        with open(kernel, 'r') as infile, open(new_filename, 'w') as outfile:
            content = infile.read()
            outfile.write(content.replace(LOCAL_PATH, local_kernel_path))

