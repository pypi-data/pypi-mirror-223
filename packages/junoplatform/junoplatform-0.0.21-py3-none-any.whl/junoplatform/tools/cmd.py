"""junoplatform.tools.cmd.py: junocli cmd implementation"""
__author__      = "Bruce.Lu"
__email__       = "lzbgt@icloud.com"
__time__ = "2023/07/20"


import click
import os
import yaml
import logging
import requests
import shutil
import traceback
import yaml
import uuid
import json
from io import StringIO
from pylint.lint import Run
from pylint.reporters.text import TextReporter
from typing import List
import zipfile
from junoplatform.io.utils import driver_cfg, get_package_path, api_url

import junoplatform
from junoplatform.meta.decorators import auth
from typing import Optional, Mapping
import collections

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s - %(message)s')
        
class CMDBase(object):
    def __init__(self):
        self.juno_dir = os.path.expanduser('~') + '/.juno'
        self.juno_file = self.juno_dir +  '/config.yaml'
        self.juno_cfg = {}
        try:
            self.juno_cfg = yaml.safe_load(open(self.juno_file, 'r'))
        except:
            pass

class OrderedGroup(click.Group):
    def __init__(self, name: Optional[str] = None, commands: Optional[Mapping[str, click.Command]] = None, **kwargs):
        super(OrderedGroup, self).__init__(name, commands, **kwargs)
        #: the registered subcommands by their exported names.
        self.commands = commands or collections.OrderedDict()

    def list_commands(self, ctx: click.Context) -> Mapping[str, click.Command]:
        return self.commands

@click.group(cls=OrderedGroup)
@click.pass_context
def main(ctx, ):
    ctx.obj = CMDBase()

pass_base = click.make_pass_decorator(CMDBase)


@main.command()
@click.argument('username')
@click.argument('password', required=False)
@pass_base
def login(base:CMDBase, username, password):
    '''must login success before all other commands
    '''
    auth = {"username": username, "password": password}
    logging.info(f"login at {api_url}")
    r = requests.post(f'{api_url}/login', data=auth, headers = {'Content-Type': 'application/x-www-form-urlencoded'})
    if r.status_code != 200:
        if 'detail' in r.json():
            detail = r.json()['detail']
            logging.error(f"login error: {detail}")
            return
        else:
            logging.error(f"login error: {r.status_code}")
    token = r.json()['access_token']
    data = {"auth": auth, "token": token}

    with open(base.juno_file, 'w') as f:
        f.write(yaml.dump(data)) 
    logging.info("successfully logged in")

@main.command()
@click.argument('name')
@click.argument('plant')
@click.argument('module')
@pass_base
@auth
def init(base, name, plant, module):
    '''create an algo module with project NAME
    '''
    home = os.path.dirname(junoplatform.__file__)
    src = f"{home}/templates/main.py"
    try:
        os.makedirs(name, exist_ok=False)
        shutil.copy2(src, name)
        doc = {"name": name, "version": "0.0.0", "author": os.getlogin(), "description": "template algo project", "plant": plant, "module": module}
        yaml.dump(doc, open(f"{name}/project.yml", "w"), sort_keys=False)
        input = {
        "tags": [
            "AI-T20502_DIS",
            "AI-T20501_DIS"
        ],
        "items": 1440,
        "sched_interval": 5
        }
        
        if plant == 'yudai':
            input["tags"] = ['AI_AT-P10503-DISP', 'COD2']

        
        if plant == 'yulin':
            input['tags'] = ['通道 1.设备 1.opc.group.3004FV00306_AI.PV', '通道 1.设备 1.opc.group.3007LIT00202_AI.PV']

        config = {"key1": 1, "key2": [1,2]}

        json.dump(input, open(f"{name}/input.json", "w"), sort_keys=False)
        json.dump(config, open(f"{name}/config.json", "w"), sort_keys=False)
    except Exception as e:
        msg = traceback.format_exc()
        logging.error(f"failed to create project {name}: {e}")

@main.command()
@pass_base
@auth
def run(base):
    '''run a package locally for testing
    '''
    os.system("python main.py")

@main.group(cls=OrderedGroup)
@click.pass_context
def package(ctx):
    pass

@main.group(cls=OrderedGroup)
@click.pass_context
def deployment(ctx):
    pass

@package.command()
@click.argument('conf_file', default="config.json")
@click.option('-t', '--tag', type=click.Choice(['algo', 'config', 'ac', 'other']), required = True)
@click.option('-m', '--message', required = True)
@click.option('-i','--input', help = "the path of input spec file", default="input.json")
@pass_base
@auth
def build(base, conf_file,  tag, message, input):
    ''' make a package and get a package_id
    '''
    try:
        logging.info(f"TODO: package {conf_file} {tag} {message} {input}")
        lint = StringIO()  # Custom open stream
        reporter = TextReporter(lint)
        Run(["main.py"], reporter=reporter, exit=False)
        errors = lint.getvalue().split("\n")
        for x in errors:
            if "failed"  in x or "fatal" in x:
                logging.error(x)
                logging.info("fix the error above and redo package")
                exit(1)

        package_id = uuid.uuid4().hex
        driver_cfg['package_id'] = package_id

        def parse_version(s:str) -> List[int]|None:
            v = s.split(".")
            if len(v) != 3:
                return None
            try:
                return [int(x) for x in v]
            except:
                return None
            
        def inc_version(v: str, t:type):
            v = parse_version(v)
            if tag == 'algo':
                v[0] +=1
                driver_cfg['tag'] = 'algo'
            elif tag == 'config':
                v[1] +=1
                driver_cfg['tag'] = 'config'
            elif tag == 'ac':
                v[0] +=1
                v[1] +=1
                driver_cfg['tag'] = 'ac'
            else:
                v[2] +=1
            driver_cfg["version"] = ".".join([str(x) for x in v])

        if "version" not in driver_cfg:
            driver_cfg["version"] = "0.0.0"
        try:
            inc_version(driver_cfg["version"], tag)
        except:
            logging.error(f"invalid version: {driver_cfg['version']}")
            exit(1)

        driver_cfg["message"] = message
            
        with open('project.yml', 'w') as f:
            yaml.safe_dump(driver_cfg, f, sort_keys=False)

        logging.info(f"pack success(new can be found in project.yml):\n\tplant: {driver_cfg['plant']}, \
                     module: {driver_cfg['module']}, conf: {conf_file}\n\t{tag}: {message}\
                     \n\tid: {package_id}\n\tversion: {driver_cfg['version']}")

        # dist
        os.makedirs("dist", exist_ok=True)
        module = driver_cfg['module']
        plant = driver_cfg['plant']
        arch = f'dist/{plant}-{module}-{driver_cfg["package_id"]}.zip'
        with zipfile.ZipFile(arch, 'w') as f:
            for root, dirs, files in os.walk('./'):
                if root[-4:] == 'dist':
                    continue
                for file in files:
                    p = os.path.join(root, file)
                    f.write(p)
                    logging.info(f"added: {p}")
        logging.info(f"package stored in: {arch}")

    except Exception as e:
        logging.error(e)

@package.command()
@click.argument('package_id', default="", required=False)
@pass_base
@auth
def upload(base, package_id):
    '''upload a package only (no deploy action)
    '''
    if not package_id:
        package_id = driver_cfg["package_id"]
    
    api = f"{api_url}/package"
    logging.info(f"upload package {package_id} to {api}")
    papath = get_package_path(driver_cfg, package_id)

    logging.info(base.juno_cfg['token'])
    
    r = requests.post(api, files = {'file': (f'{package_id}.zip', open(papath, 'rb'), 'application/zip')}, headers={"Authorization": f"Bearer {base.juno_cfg['token']}"})
    if r.status_code != 200:
        msg = f"faild upload package {package_id} "
        if "detail" in r.json():
            msg += r.json()["detail"]
        logging.error(msg)
    else:
        logging.info(f"successfully upload package {package_id}")

def _deploy(base:CMDBase, package_id: str =""):
    pass

@package.command()
@click.argument('id')
@pass_base
@auth
def deploy(base, id):
    '''deploy package
    '''
    logging.info(f"TODO: deploy {id}")

@package.command()
@click.argument('plant', required=False)
@pass_base
@auth
def list(base, plant):
    '''list packages and deployed status
    '''
    logging.info(f"TODO: list {plant}")

@package.command()
@click.argument('plant')
@click.argument('module')
@click.argument('id', required=False)
@pass_base
@auth
def rollback(base, plant, module, id):
    '''rollback a package to previous version or specific id[optional]
    '''
    logging.info(f"TODO: rollback {plant} {module} {id}")

@deployment.command()
@click.argument('plant')
@click.argument('module', required = False)
@pass_base
@auth
def list(base, plant, module):
    ''' check package status
    '''
    logging.info(f"TODO: status {id}")


@deployment.command()
@click.argument('deployment_id')
@pass_base
@auth
def status(base, plant, module):
    ''' check package status
    '''
    logging.info(f"TODO: status {id}")