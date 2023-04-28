class Environment:
    @staticmethod
    def is_jupyter():
        try:
            get_ipython()
            return True
        except NameError:
            return False
