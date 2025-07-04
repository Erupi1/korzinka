import os

folders = [
    'dialogs',
    'ui',
    'resources',
    os.path.join('resources', 'icons'),
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

print('Папки созданы.') 