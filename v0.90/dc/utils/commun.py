import os
import json
import string
import random
import shutil
import time
from time import mktime
from datetime import timedelta
from datetime import datetime


class Commun:
    """Commun unspecific funcs """

    upper = list(string.ascii_uppercase)
    lower = list(string.ascii_lowercase)
    numbers = list(string.digits)
    characters_list = upper + lower + numbers

    def read_json(self, filepath):
        """Return a dict form a json file"""
        with open(filepath) as j:
            adict = json.load(j)
        return adict

    def write_json(self, thedict, thepath, fname=None):
        """Write dict to Json file"""
        if fname != None:
            thepath = os.path.join(thepath, fname)

        with open(thepath, "w") as f:
            #Write to file
            json.dump(thedict, f)
    
    def config_info(self):
        """Get as a dict the config.json file"""
        info_dict = self.read_json('config.json')
        return info_dict


    def generate_id(self, len_id):
        """Generate a random series of chars upper/lower + numbers"""
        custom_id = []
        for _ in range(len_id):
            custom_id.append(random.choice(self.characters_list))
        custom_id_result = ''.join(custom_id)
        return custom_id_result


    def current_date(self, date_format='%Y-%m-%d'):
        """Get current date in year-month-day format(default)"""
        date = datetime.now().strftime(date_format)
        return date


    def wait_file_on_disk(self, save_path_file, timeout=900):
        """Wait file to be saved in the path specified on disk"""
        wait_until = datetime.now() + timedelta(seconds=timeout)
        while os.path.isfile(save_path_file) != True:
            if wait_until < datetime.now():
                raise ValueError("Timeout reached!")
            time.sleep(1)

    def copy_dirs(self, src, dst, symlinks=False, ignore=None):
        """Copy dirs and it's items from src to dst"""
        if not os.path.exists(dst):
            os.makedirs(dst)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                self.copy_dirs(s, d, symlinks, ignore)
            else:
                if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                    shutil.copy2(s, d)

    def delete_dirs(self, apath):
        """Delete directory and all it's subfolders"""
        try:
            shutil.rmtree(apath) #delete folders, subfolders and files
        except:
            shutil.rmtree(apath, ignore_errors=True) #delete files that are not opened
            raise Exception("Not all files were deleted from {}".format(apath))


    def listify_string(self, astring, delimiter=','):
        """Make a list from a string spliting it by it's delimiter"""
        strListifyed = astring.split(delimiter)
        astringListifyed = [s.strip() for s in strListifyed]
        return astringListifyed


    def list_path_to_files(self, root_path):
        """Walk thru a start path and return a list of paths to files"""

        allfiles = []
        for root, _, files in os.walk(root_path):
            for f in files:
                path_tofile = os.path.join(root, f)
                allfiles.append(path_tofile)
        
        return allfiles


    def list_duplicates(self, seq):
        """Check for duplicates"""
        seen = set()
        seen_add = seen.add
        # adds all elements it doesn't know yet to seen and all other to seen_twice
        seen_twice = set( x for x in seq if x in seen or seen_add(x) )
        # turn the set into a list (as requested)
        return list(seen_twice)


    def get_unique_list(self, seq):
        """Get a uniques list but peserve order"""
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]


    def get_file_size_mtime(self, filepath):
        """Get file size in bytes and modification date"""
        metadata = os.stat(filepath)
        file_size = str(metadata.st_size) # bytes
        filetime = time.localtime(metadata.st_mtime)
        dt = datetime.fromtimestamp(mktime(filetime))
        creation_date = dt.strftime('%d-%m-%Y')

        fileinfodict = {'FileSizeBytes':file_size,
                        'ModificationDate': creation_date
                        }

        return fileinfodict
