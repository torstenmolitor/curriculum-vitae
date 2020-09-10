import os


class Compiler:
    pass


class PdfLatex(Compiler):
    def compile_command(self, job_name):
        if job_name == '':
            return 'pdflatex'
        else:
            return f'pdflatex -jobname={job_name}'


class LatexMake(Compiler):
    def __str__(self):
        return 'latexmk'


class Document:
    def __init__(self, document_name, job_name='', compiler=PdfLatex):
        self.document_name = document_name
        self.job_name = job_name
        self.compiler = compiler()

    def compile(self):
        os.system(f'{self.compiler.compile_command(job_name=self.job_name)} {self.document_name}')
