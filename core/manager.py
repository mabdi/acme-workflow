from flask_script import Command, Manager, Option


class MinitManager(Command):
    option_list = (
        Option('--name', '-n', dest='name'),
    )

    def run(self, name):
        print("Minit actions goes here, param :%s" % name)
