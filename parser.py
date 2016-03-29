
class FileParser(object):
    def __init__(self, data_dir, specs_dir):
        self.data_dir = data_dir
        self.specs_dir = specs_dir

    def __call__(self, one_pass=True):
        while True:
            print('running')
            if one_pass:
                break