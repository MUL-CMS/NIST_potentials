from lxml import html
import os

def split_path(path):
    head, tail = os.path.split(path)
    if head == '':
        return [tail]
    return split_path(head) + [tail]

def enter_subfolder(path, pot_path):
    if len(path) == 1:
        # final subfolder, let's download if the file doesn't exist
        if not os.path.exists(path[0]):
            os.system(f'wget {pot_path}')
        else:
            print(f'<{pot_path}> exists, skipping download')
    else:
        folder = path.pop(0)
        if not os.path.exists(folder):
            os.mkdir(folder)
        os.chdir(folder)
        enter_subfolder(path, pot_path)


NIST_ROOT = 'https://www.ctcms.nist.gov/potentials/Download'
os.system(f'wget {NIST_ROOT}')
CWD = os.getcwd()

with open('Download', 'r', encoding='utf-8') as inp:
    htmldoc = html.fromstring(inp.read()) 
pots = htmldoc.find_class('panel-body')[0][0]
for pot in pots[:]:
    pot = str(html.tostring(pot[0])).split('"')[1][2:]
    if 'orkshop' not in pot:
        path = (split_path(pot))
        os.chdir(CWD)
        enter_subfolder(path, f'{NIST_ROOT}/{pot}')

os.chdir(CWD)    
os.system('rm Download')
os.system('touch _last_download.timestamp')
