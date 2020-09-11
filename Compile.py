import os
from string import Template


class Compiler:
    pass


class PdfLatex(Compiler):

    def compile_command(self, job_name):
        if job_name == '':
            return 'pdflatex'
        else:
            return f'pdflatex -jobname={job_name}'


class LatexMake(Compiler):

    def compile_command(self):
        return 'latexmk'

    def clean(self):
        return os.system(self.compile_command() + ' -C')


class Document:
    def __init__(self, document_name='main', job_name='main', compiler=PdfLatex()):
        self.document_name = document_name
        self.job_name = job_name
        self.compiler = compiler

    def compile(self, geometry=None, job_name=None):
        """Compiles the Latex document to a pdf"""

        if geometry is not None:
            self.set_params(geometry)

        if job_name is None:
            job_name = self.job_name

        os.system(f'{self.compiler.compile_command(job_name=job_name)} {self.document_name}')

        return job_name + '.pdf'

    def set_params(self, geometry):
        """Arranges the main document to use dynamic params and
         substitutes the specified geometry into the geometry template"""

        with open(self.document_name + '.tex', 'r') as main:
            contents_main = main.read()

        new_contents_main = contents_main.replace('geometry-default', 'geometry-dynamic')
        self.document_name = 'main-dynamic'

        with open(self.document_name + '.tex', 'w') as main:
            main.write(new_contents_main)

        with open('geometry-dynamic-template.tex', 'r') as file:
            dynamic_geometry = Template(template=file.read()).substitute(**geometry)

        with open('geometry-dynamic.tex', 'w') as file:
            file.write(dynamic_geometry)


