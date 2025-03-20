from glob import glob
import os
import yaml

# Splits a file path into its components recursively
def split_path(path):
    head, tail = os.path.split(path)
    return split_path(head) + [tail] if head else [tail]

# Creates a folder if it doesn't exist and changes to it
def cd(folder):
    os.makedirs(folder, exist_ok=True)
    os.chdir(folder)

# Get the current working directory
ROOT = os.getcwd()
model = "eam.alloy"

# Create the model directory if it doesn't exist
os.makedirs(model, exist_ok=True)

# List to store potential files information
potentials = []

# Find all directories matching the format 'year--<whatever>' (e.g., 2015--example)
folders = glob('[1-2][0-9][0-9][0-9]--*')
for f in folders:
    os.chdir(f)
    for v in glob('*'):
        os.chdir(v)
        for pot in glob(f'*{model}'):
            elements = f.split('--')[-1].split('-')  # Extract element names from folder name
            potentials.append([f, v, pot, elements])
        os.chdir('..')
    os.chdir('..')

# Move to the model directory
cd(model)
model_ROOT = os.getcwd()

# Process and store potential file data
pots = []
for pot in potentials:
    os.chdir(model_ROOT)
    cd(pot[0])  # Create and navigate to subdirectory
    cd(pot[1])
    
    # Copy potential file to the target location
    src_path = os.path.join(ROOT, *pot[:-1])
    dest_path = os.path.join(model_ROOT, *pot[:-2])
    os.system(f'cp {src_path} {dest_path}')
    
    # Sort element names and remove numeric prefixes if any
    elements = sorted(pot[-1])
    while elements and elements[0].isdecimal():
        elements.pop(0)
    
    # Store potential metadata
    pots.append({
        'pot_file': os.path.join(*pot[:-1]),
        'elements': elements
    })

# Store the final potential data structure in a YAML file
pot_data = {
    'pot_root': model_ROOT,
    'potentials': pots
}

os.chdir(model_ROOT)
with open('potentials.yaml', 'w') as f:
    yaml.dump(pot_data, f)

print("Potential data saved to potentials.yaml")
