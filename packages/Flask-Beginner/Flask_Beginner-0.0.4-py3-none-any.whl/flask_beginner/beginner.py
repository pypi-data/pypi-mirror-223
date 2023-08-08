import os
import argparse

class cd:
    """a simple cd command"""
    def __init__(self,newdir):
        self.newdir = newdir
        
    def __enter__(self):
        self.savapath = os.getcwd()
        if not os.path.exists(self.newdir):
            os.makedirs(self.newdir)
        os.chdir(self.newdir)

    def __exit__(self, etype, value, traceback):
        os.chdir('..')


def create_file(filename,content = ''):
    if not os.path.exists(filename):
        with open(filename,'w') as f:
            if content:
                f.write(content)


def make_project_files():
    create_file('.gitignore',
                content='.env\nenv\n.history\n*.pyc\n__pycache__\n'
                )
    create_file('README.md')
    create_file('requirements.txt')
    create_file('wsgi.py')
    create_file('test.py')


def make_app(name='app'):
    """make app package"""
    
    with cd(name):
        create_file('__init__.py')
        create_file('models.py')
        create_file('extensions.py')
        create_file('forms.py')
        create_file('settings.py')
        
        with cd('blueprints'):
            create_file('__init__.py')
        
        with cd('static'):
            create_file('style.css')
            with cd('img'):
                pass
        
        with cd('templates'):
            create_file('base.html')
            with cd('errors'):
                create_file('404.html')
                create_file('400.html')
                create_file('500.html')
        

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
    make_project_files()
    
    
    

