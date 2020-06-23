#!/usr/bin/env python                                            
#
# medcon ds ChRIS plugin app
#
# (c) 2016-2019 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#


import os
import sys
import subprocess
sys.path.append(os.path.dirname(__file__))

# import the Chris app superclass
from chrisapp.base import ChrisApp


Gstr_title = """

Generate a title from 
http://patorjk.com/software/taag/#p=display&f=Doom&t=medcon

"""

Gstr_synopsis = """

(Edit this in-line help for app specifics. At a minimum, the 
flags below are supported -- in the case of DS apps, both
positional arguments <inputDir> and <outputDir>; for FS apps
only <outputDir> -- and similarly for <in> <out> directories
where necessary.)

    NAME

       medcon.py 

    SYNOPSIS

        python medcon.py                                         \\
	    -i | --inputFile						\\
	    [-a]  [--args]						\\
	    [-do]      							\\
            [-h] [--help]                                               \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            <inputDir>                                                  \\
            <outputDir> 

    BRIEF EXAMPLE

        * Bare bones execution

            mkdir in out && chmod 777 out
            python medcon.py   \\
                                in    out

    DESCRIPTION

        `medcon.py` 

    ARGS

	-i | --inputFile
	Input file to process. This file exists within the explictly provided CLI
	positional <inputDir>.
	
	[-a]  [--args]	
	Optional string of additional arguments to "pass through" to medcon.

	All the args for medcon are themselves specified at the plugin level with this flag. These
	args MUST be contained within single quotes (to protect them from the shell) and
	the quoted string MUST start with the required keyword 'ARGS: '.
	
	[-do]  
	Optional argument which an specify a conversion from one type to another. 
	Currently, only supports conversion from NIfTI to DICOM by passing the string "nifti2dicom" 
	
        [-h] [--help]
        If specified, show help message and exit.
        
        [--json]
        If specified, show json representation of app and exit.
        
        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta data and exit.
        
        [--savejson <DIR>] 
        If specified, save json representation file to DIR and exit. 
        
        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.
        
        [--version]
        If specified, print version number and exit. 

"""


class Medcon(ChrisApp):
    """
    An app to ....
    """
    AUTHORS                 = 'Arushi Vyas (dev@babyMRI.org)'
    SELFPATH                = os.path.dirname(os.path.abspath(__file__))
    SELFEXEC                = os.path.basename(__file__)
    EXECSHELL               = 'python3'
    TITLE                   = 'A ds plugin to convert NIfTI to DICOM'
    CATEGORY                = ''
    TYPE                    = 'ds'
    DESCRIPTION             = 'An app to ...'
    DOCUMENTATION           = 'http://wiki'
    VERSION                 = '0.1'
    ICON                    = '' # url of an icon image
    LICENSE                 = 'Opensource (MIT)'
    MAX_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MAX_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT           = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT           = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """

        self.add_argument("-a", "--args",
                          help="medcon arguments to pass",
                          type=str,
                          dest='args',
                          optional=True,
                          default="")
        self.add_argument("-do",
                          help="functionality of medcon to be used",
                          type=str,
                          dest='do',
                          optional=True,
                          default="nifti2dicom")
        self.add_argument("-i", "--inputFile", #equivalent to -f of medcon
                          help="input file",
                          type=str,
                          dest='inputFile',
                          optional=False,
                          default="")
        # self.add_argument("-o", "--outputFile",
        #                   help="output file",
        #                   type=str,
        #                   dest='outputFile',
        #                   optional=False,
        #                   default="")

    def job_run(self, str_cmd):
        """
        Running some CLI process via python is cumbersome. The typical/easy 
        path of

                            os.system(str_cmd)

        is deprecated and prone to hidden complexity. The preferred
        method is via subprocess, which has a cumbersome processing
        syntax. Still, this method runs the `str_cmd` and returns the
        stderr and stdout strings as well as a returncode.

        Providing readtime output of both stdout and stderr seems
        problematic. The approach here is to provide realtime
        output on stdout and only provide stderr on process completion.

        """
        d_ret = {
            'stdout':       "",
            'stderr':       "",
            'returncode':   0
        }

        p = subprocess.Popen(
                    str_cmd.split(),
                    stdout      = subprocess.PIPE,
                    stderr      = subprocess.PIPE,
        )

        # Realtime output on stdout
        str_stdoutLine  = ""
        str_stdout      = ""
        while True:
            stdout      = p.stdout.readline()
            if p.poll() is not None:
                break
            if stdout:
                str_stdoutLine = stdout.decode()
                print(str_stdoutLine, end = '')
                str_stdout      += str_stdoutLine
        d_ret['stdout']     = str_stdout
        d_ret['stderr']     = p.stderr.read().decode()
        d_ret['returncode'] = p.returncode
        print('\nstderr: \n%s' % d_ret['stderr'])
        return d_ret

    def job_stdwrite(self, d_job, options):
        """
        Capture the d_job entries to respective files.
        """
        for key in d_job.keys():
            with open(
                #'%s/%s-%s' % (options.outputdir, options.outputFile, key), "w"
		 '%s-%s' % (options.outputdir, key), "w"
            ) as f:
                f.write(str(d_job[key]))
                f.close()
        return {
            'status': True
        }

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """

        global str_cmd
        print(Gstr_title)
        print('Version: %s' % self.get_version())

        l_appargs = options.args.split('ARGS:')
        if len(l_appargs) == 2:
            str_args = l_appargs[1]
        else:
            str_args = l_appargs[0]

        if len(options.do):
            if options.do == 'nifti2dicom':
                options.args += "-c dicom -split3d"

        print('%s/%s' % (options.inputdir, options.inputFile))
        print('%s' % options.outputdir)
        print(options.args)
        
        os.chdir(options.outputdir)
        str_cmd = "medcon -f %s/%s %s" % (options.outputdir, options.inputdir, options.inputFile, str_args)

        # Run the job and provide realtime stdout
        # and post-run stderr
        self.job_stdwrite(
            self.job_run(str_cmd), options
        ) 

	
        
    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)


# ENTRYPOINT
if __name__ == "__main__":
    chris_app = Medcon()
    chris_app.launch()
