import os
from dc.utils.commun import Commun


class Folders:
    """Creation/manipulation of folders for this app"""

    cwd = os.getcwd()
    com = Commun()

    def create_needed_dirs(self):
        """Create the working directories if doesn't exist"""

        root_path = os.path.join(self.cwd, 'DC BATCHES IN WORK')

        sub_folders = ['0 NEW',
                    '1 UNASSIGNED',
                    '2 PREPARED FILES',
                    '3 ASSIGNED',
                    '4 TO BE CHECKED',
                    '5 TO BE IMPORTED',
                    '6 FINISHED',
                    '7 IN STANDBY',
                    '8 UNRECORDABLE']

        extraDirs = [root_path, 'excels exported', 'excels to be imported', 'FUDB', 'bin']

        for extradir in extraDirs:
            try:
                os.mkdir(extradir)
            except:
                pass

        for adir in sub_folders:
            subdir = os.path.join(root_path, adir)
            try:
                os.mkdir(subdir)
            except:
                pass



    def defaultconfig(self):
        """"Create default config.json file"""

        config_data = {
                "path_to_database": "FUDB/FOLLOWUP.DB",
                "path_to_frontend": "FUDB/",
                "path_to_dcs_info": "FUDB/",
                "path_to_bin": "bin/",
                "path_to_excels_exported_from_database": "excels exported/",
                "path_to_excels_to_be_imported_in_database": "excels to be imported/",
                "path_to_new_opfiles": "DC BATCHES IN WORK/0 NEW/",
                "path_to_batches_unassigned": "DC BATCHES IN WORK/1 UNASSIGNED/",
                "path_to_batches_prepfiles": "DC BATCHES IN WORK/2 PREPARED FILES/",
                "path_to_batches_assigned": "DC BATCHES IN WORK/3 ASSIGNED/",
                "path_to_batches_tobechecked": "DC BATCHES IN WORK/4 TO BE CHECKED/",
                "path_to_batches_tbimported": "DC BATCHES IN WORK/5 TO BE IMPORTED/",
                "path_to_batches_finished": "DC BATCHES IN WORK/6 FINISHED/",
                "path_to_batches_instandby": "DC BATCHES IN WORK/7 IN STANDBY/",
                "path_to_batches_unrecordable": "DC BATCHES IN WORK/8 UNRECORDABLE/",
                "batch_status_options_responsible": "PREP. OP FILE, IMPORTATION & SPLIT FILE, RELIABILITY & DATA UPGRADE, CHECK OP FILE, CHECK SPLIT FILE, CHECK FRONT END, **TO BE CHECKED",
                "batch_status_options_proofreader": "OP FILE OK, SPLIT FILE OK, FRONT END OK, **TO BE IMPORTED, **FINISHED, **REWORK, **STANDBY, **UNRECORDABLE",
                "batch_status_options_overall": "ONGOING, STANDBY, FINISHED, UNRECORDABLE",
                "aircraft": "A300, A300-600, A310, A320, A330, A340, A350, A380",
                "split_batch_factor": "2, 3, 4, 5, 6, 7, 8, 9",
                "generateBigID": "NO",
                "generateCustomID": "YES",
                "customIDlentgh": "6"
            }
        
        if not os.path.isfile(os.path.join(self.cwd, "config.json")):
            self.com.write_json(config_data, self.cwd, fname="config.json")



    def make_default_dirs(self):
        """Create default dirs and config.json if needed"""

        self.defaultconfig()
        self.create_needed_dirs()

