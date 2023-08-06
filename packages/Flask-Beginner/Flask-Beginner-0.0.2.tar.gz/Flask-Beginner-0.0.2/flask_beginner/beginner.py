import os
import argparse

class cd:
    """a simple cd command"""
    def __init__(self,newdir):
        self.newdir = newdir
        
    def __enter__(self):
        self.savapath = os.getcwd()
        os.makedirs(self.newdir)
        os.chdir(self.newdir)

    def __exit__(self, etype, value, traceback):
        os.chdir('..')


def create_gitigonore():
    """make .gitignore"""
    with open('.gitignore','w') as f:
        f.write('.env\n')
        f.write('.history\n')
        f.write('env\n')
        f.write('*.pyc\n')
        f.write('__pycache__\n')


def create_readme():
    """make README.md"""
    with open('README.md','w') as f:
        pass


def create_requirements():
    """make requirements.txt"""
    with open('requirements.txt','w') as f:
        f.writelines('Flask')

def create_wsgi():
    with open('wsgi.py','w') as f:
        pass

def create_test():
    with open('test.py','w') as f:
        pass


def make_app(name='app'):
    """make app package"""
    
    with cd(name):
        with open('__init__.py','w') as f:
            pass
        
        with open('models.py','w') as f:
            pass
        
        with open('extensions.py','w') as f:
            pass
        
        with open('forms.py','w') as f:
            pass
        
        with open('settings.py','w') as f:
            pass
        
        with cd('blueprints'):
            with open('__init__.py','w'):
                pass
        
        with cd('static'):
            pass
        
        with cd('templates'):
            pass


def run():
    """
        flask go!!!!!!
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-n','--name',help='the name for your app package')
    args = parser.parse_args()
    if args.name:
        app_name = args.name
        make_app(app_name)
    else:
        make_app()
    create_gitigonore()
    create_readme()
    create_requirements()
    create_wsgi()
    create_test()
    

