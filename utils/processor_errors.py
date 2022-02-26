class ProcessorError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print('calling str')
        if self.message:
            return '{}, {} '.format(self.__name__, self.message)
        else:
            return '{} has been raised'.format(self.__name__)


class DataTypeProcessorError(ProcessorError):
    pass


class FormatFieldsProcessorError(ProcessorError):
    pass
