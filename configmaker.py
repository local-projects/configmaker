from optparse import OptionParser
import os
import re

class Variables(object):
    def __init__(self, rckeys=None):
        self.vars = rckeys or {}
        
    def __getitem__(self, k):

        v = raw_input("\tEnter value for '%s' [%s]: " % (k, self.vars.get(k, "")))
        if not v and self.vars.get(k) is not None:
            v = self.vars.get(k)
        
        self.vars[k] = v

        return v

def kv_from_file(rcfile):
    kv = {}
    with open(rcfile, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith("#"):
                continue
            if len(line) == 0:
                continue
            re.sub("#.*", "", line)
            line.strip()
            k,v = line.split("=")
            kv[k.strip()] = v.strip()
        
    return kv

def extract_configs(config_file, rc_file, config_template):    
    conffile = open(config_file, "w")
    rckeys = {}
    
    if os.path.exists(rc_file):
        # First extract out all the kv pairs from the existing rcfile
        rckeys = kv_from_file(rc_file)
    
    print ("Assign values to the different variables. \n"
           "Values may be blank (just hit enter). Booleans must be True/False \n"
           "These will be written out to %s and the configuration file will be %s" %
           (rc_file, config_file))
    
    myvars = Variables(rckeys)
    with open(os.path.expanduser(config_template), "r") as f:
        for line in f.readlines():
            try:
                out = line % myvars
                conffile.write(out)
            except Exception as exc:
                raise
            
    # Now write out all the variables to rcfile
    with open(os.path.expanduser(rc_file), "w") as rc:
        for k,v in myvars.vars.items():
            rc.write("%s: %s\n" % (k,v))
    

if __name__ == "__main__":
    """Run config file generator"""
    parser = OptionParser()

    parser.add_option("--config_file", 
                  help="Write final configuration into this file.")
    parser.add_option("--rc_file", 
                  help="Write out variables into this rcfile.")
    parser.add_option("--template", 
                  help="Template file (usually config.yml.tmpl) to start from.")
    (options, args) = parser.parse_args()

    while not options.template or not os.path.exists(os.path.expanduser(options.template)):
        ans = raw_input("Template file to read from: ")
        if os.path.exists(os.path.expanduser(ans)):
            options.template = ans
            break
    
    # If the rcfile already exists, use it as the starting point, and append
    while not options.rc_file: 
        ans = raw_input("Full path to rcfile to save to: ")
        ans = ans.strip()

        path = os.path.split(os.path.expanduser(ans))[0]
        if os.path.exists(os.path.expanduser(path)):
            options.rc_file = ans
            break
        else:
            print("Path %s does not exist. Please create it before proceeding, or provide new path." % path)
        
    while not options.config_file:
        ans = raw_input("Full path to config.yml to save to: ")
        path = os.path.split(os.path.expanduser(ans))[0]
        if os.path.exists(path):
            options.config_file = ans
            break
        else:
            print("Path %s does not exist. Please create it before proceeding, or provide new path." % path)

    if os.path.exists(os.path.expanduser(options.config_file)):
        ans = raw_input("File %s already exists. Will delete and replace file. Ok? [y/n] " % options.config_file)
        if not ans.lower().startswith("y"):
            print "Please use a different target config file."
            exit(1)
            
    # Validate the paths
    options.rc_file = os.path.expanduser(options.rc_file)
    options.config_file = os.path.expanduser(options.config_file)
    extract_configs(options.config_file, options.rc_file, options.template)
    
