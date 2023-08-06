import tempfile
import os
import subprocess

class TeXUtils:
    def __init__(self, tex_src, job_name: str, dir_name: str = ''):
        self.tex = tex_src
        self.params = dict()
        self.params['-jobname'] = job_name
        self.params['-output-directory'] = dir_name

    @classmethod
    def from_tex_file(cls, filename):
        dir_name = os.path.dirname(filename)
        prefix = os.path.basename(filename)
        prefix = os.path.splitext(prefix)[0]
        with open(filename, 'rb') as f:
            return cls.from_binary_string(f.read(), prefix, dir_name)

    @classmethod
    def from_binary_string(cls, binstr, jobname: str, dir_name: str = None):
        return cls(binstr, jobname, dir_name)

    def create_pdf(self, keep_pdf: bool = False, keep_log: bool = False, env: dict = None):
        args = self.get_args()
        subprocess.run(['pdflatex', *args], input=self.tex)

    def get_args(self):
        return [k+('='+v if v is not None else '') for k, v in self.params.items()]