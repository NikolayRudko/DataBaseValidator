class ProcessorError(Exception):
    pass


class DataTypeProcessorError(ProcessorError):
    pass


class FormatFieldsProcessorError(ProcessorError):
    pass


class ArrivalTimeProcessorError(ProcessorError):
    pass
