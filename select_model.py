from glob import glob
import os
import yaml

def split_path(path):
    head, tail = os.path.split(path)
    if head == '':
        return [tail]
    return split_path(head) + [tail]

def cd(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)
    os.chdir(folder)
  
ROOT = os.getcwd()
model = "eam.fs"
if not os.path.exists(model):
    os.mkdir(model)


potentials = []
folders = glob(f'[1-2][0-9][0-9][0-9]--*') # format year--<whatever>
for f in folders:
    os.chdir(f)
    for v in glob('*'):
        os.chdir(v)
        for pot in glob(f'*{model}'):
            # print(pot)
            el = f.split('--')[-1].split('-')
            potentials.append([f, v, pot, el])
        os.chdir('..')
    os.chdir('..')

cd(model)
model_ROOT = os.getcwd()
    
pots = []
for pot in potentials:
    os.chdir(model_ROOT)
    cd(pot[0])
    cd(pot[1])
    os.system(f'cp {os.path.join(ROOT, *pot[:-1])} {os.path.join(model_ROOT, *pot[:-2])}')
    el = sorted(pot[-1])
    while str.isdecimal(el[0]):
        el.pop(0)
    pots.append(dict(
        pot_file = os.path.join(*pot[:-1]),
        elements = el
    ))

pot_data = dict(
    pot_root = model_ROOT,
    potentials = pots
)

os.chdir(model_ROOT)
with open('potentials.yaml', 'w') as f:
    f.write(yaml.dump(pot_data))