import yaml
import os


class Conf:
    ins = None

    @staticmethod
    def get_conf():
        return Conf._singleton_load_conf()

    @staticmethod
    def _singleton_load_conf():
        if Conf.ins is None:
            with open(
                    os.path.join(
                        os.path.dirname(__file__)
                        , 'settings.yaml')
            ) as fp:
                data = yaml.load(fp, Loader=yaml.FullLoader)
                Conf.ins = data
                return Conf.ins
        else:
            return Conf.ins
