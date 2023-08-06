from deairequest.connectors.bacalhau import notebooks, backends
import tempfile
from pathlib import Path

def main(notebook:Path, name:str, imagetag:str, pythonversion:str, datasets:list(dict()), cpu:str, gpu:str, memory:str)->str:

    target=tempfile.mkdtemp()
    config = dict({
        'notebook':{
            'name': name
        },
        'environments':{
            'default':{
                'image_tag': imagetag,
                'python': pythonversion
            }
        },
        'datasources':datasets,
        'resources':{
            'cpu': cpu,
            'gpu': gpu,
            'memory': memory
        }
    })
    base_path, root_file = notebooks.compile(notebook, target, config)
    return backends.bdeploy(base_path, root_file, config)

if __name__ == "__main__":
    main()