import logging
import os
from persiantools.jdatetime import JalaliDate
import datetime
from functools import wraps


class errors_and_warnings:
    """Contains static methods that return error and warning messages for logging."""

    @staticmethod
    def undefined_date_type() -> str:
        """Returns an error message indicating that the given date type is undefined."""

        return "The given date type is undefined. select a type from date_types class."

    @staticmethod
    def undefined_date_format() -> str:
        """Returns an error message indicating that the given date format is undefined."""

        return "The given date format is undefined. select a format from date_formats class."

    @staticmethod
    def undefined_time_format() -> str:
        """Returns an error message indicating that the given time format is undefined."""

        return "The given time format is undefined. select a format from time_formats class."

    @staticmethod
    def undefined_log_level() -> str:
        """Returns an error message indicating that the given log level is undefined."""
        
        return "The given log level is undefined. select a level from log_levels class."

    @staticmethod
    def incorrect_message_datatype() -> str:
        """Returns an error message indicating that the given message must be an instance of the log_message class."""

        return "The given message must be an instance of the log_message class."

    @staticmethod
    def incorrect_key_datatype() -> str:
        """Returns an error message indicating that the given key must be a string."""

        return "The given key must be a string."

    @staticmethod
    def defined_key() -> str:
        """Returns a warning message indicating that the given key is already defined."""

        return "The given key is already defined."

    @staticmethod
    def incorrect_input_datatype() -> str:
        """Returns an error message indicating that the given input must be a string or an instance of the log_message class."""

        return "The given input must be string or an instance of the log_message class."

    @staticmethod
    def undefined_key() -> str:
        """Returns an error message indicating that the given key is undefined."""
        
        return "The given key is undefined."

class date_types:
    """Defines different types of date formats."""

    SOLAR_DATE = 'Solar'
    AD_DATE = 'AD'

class date_formats:
    """Defines different formats for representing dates."""

    MMDDYY = "MMDDYY"
    DDMMYY = "DDMMYY"
    YYMMDD = "YYMMDD"

class time_formats:
    """Defines different formats for representing time."""

    HHMM = "HHMM",
    HHMMSS = "HHMMSS",
    HHMMSSMM = "HHMMSSMM"

class log_levels:
    """Defines different log levels."""

    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
    EXCEPTION = 60

class date:
    def __init__(self, date_type: str = date_types.AD_DATE, date_format: str = date_formats.YYMMDD) -> None:
        """Initialize the date object with the specified date type and format.

        Args:
            date_type (str, optional): The type of date to be used (AD_DATE or SOLAR_DATE). Defaults to date_types.AD_DATE.
            date_format (str, optional): The format of the date (YYMMDD, DDMMYY, or MMDDYY). Defaults to date_formats.YYMMDD.
        """
        
        self.year = 0
        self.month = 0
        self.day = 0

        self.set_date_type(date_type)
        self.set_date_format(date_format)

    def set_date_type(self, type: str) -> None:
        """Set the date type for the date object.

        Args:
            type (str): The type of date (AD_DATE or SOLAR_DATE).
        """

        types = [v for k, v in vars(date_types).items() if not(k.startswith('__'))]
        assert type in types, errors_and_warnings.undefined_date_type()
        self.date_type = type

    def set_date_format(self, format: str) -> None:
        """Set the date format for the date object.

        Args:
            format (str): The format of the date (YYMMDD, DDMMYY, or MMDDYY).
        """

        formats = [v for k, v in vars(date_formats).items() if not(k.startswith('__'))]
        assert format in formats, errors_and_warnings.undefined_date_format()
        self.date_format = format

    def update_date(self) -> None:
        """Update the date attributes based on the selected date type.

        If the date type is SOLAR_DATE, the attributes will be updated with the current Jalali date.
        If the date type is AD_DATE, the attributes will be updated with the current Gregorian date.
        """

        if self.date_type == date_types.SOLAR_DATE:
            self.day = JalaliDate.today().day
            self.month = JalaliDate.today().month
            self.year = JalaliDate.today().year

        elif self.date_type == date_types.AD_DATE:
            self.day = datetime.datetime.today().date().day
            self.month = datetime.datetime.today().date().month
            self.year = datetime.datetime.today().date().year

    def get_date_string(self, sep: str = '-') -> str:
        """Get the date string representation based on the selected date format.

        Args:
            sep (str, optional): The separator to be used between date components. Defaults to '-'.

        Returns:
            str: The date string representation.
        """
                
        self.update_date()

        if self.day < 10:
            day = '0' + str(self.day)
        else:
            day = str(self.day)

        if self.month < 10:
            month = '0' + str(self.month)
        else:
            month = str(self.month)

        year = str(self.year)

        if self.date_format == date_formats.YYMMDD:
            date = '%s%s%s%s%s' % (year, sep, month, sep, day)
        elif self.date_format == date_formats.DDMMYY:
            date = '%s%s%s%s%s' % (day, sep, month, sep, year)
        elif self.date_format == date_formats.MMDDYY:
            date = '%s%s%s%s%s' % (month, sep, day, sep, year)

        return date

class time:
    def __init__(self, time_format=time_formats.HHMMSS):
        """Initialize the time object with the specified time format.

        Args:
            time_format (str, optional): The format of the time. Defaults to time_formats.HHMMSS.
        """

        self.time = datetime.datetime.now()
        self.set_time_format(time_format)

    def set_time_format(self, format):
        """Set the time format for the time object.

        Args:
            format (str): The format of the time (HHMM, HHMMSS, or HHMMSSMM).
        """

        formats = [v for k, v in vars(time_formats).items() if not(k.startswith('__'))]
        assert format in formats, errors_and_warnings.undefined_time_format()
        self.time_format = format

    def update_time(self):
        """Update the current time.
        """
        
        self.time = datetime.datetime.now()

    def get_time_string(self, sep='-'):
        """Get the time string representation based on the selected time format.

        Args:
            sep (str): The separator for the time components (default: '-').

        Returns:
            str: The time string representation.
        """

        self.update_time()
        if self.time_format == time_formats.HHMM:
            time = str(self.time.strftime("%H{}%M".format(sep)))
        elif self.time_format == time_formats.HHMMSS:
            time = str(self.time.strftime("%H{}%M{}%S".format(sep, sep)))
        elif self.time_format == time_formats.HHMMSSMM:
            time = str(self.time.strftime("%H{}%M{}%S.%f".format(sep, sep)))

        return time

class log_message:
    def __init__(self, level: int, text: str, code: str = None) -> None:
        """Initializes a log message object with the specified level, text, and optional code.

        Args:
            level (int): The level of the log message.
            text (str): The text of the log message.
            code (str, optional): The code associated with the log message. Defaults to None.
        """

        self.set_level(level)
        self.set_text(text)
        self.set_code(code)

    def set_level(self, level: int) -> None:
        """Sets the level of the log message.

        Args:
            level (int): The level of the log message.
        """

        self.level = level

    def set_text(self, text: str) -> None:
        """Sets the text of the log message.

        Args:
            text (str): The text of the log message.
        """

        self.text = text

    def set_code(self, code) -> None:
        """Sets the code associated with the log message.

        Args:
            code: The code associated with the log message.
        """

        self.code = code

    def get_message(self) -> str:
        """ Returns the formatted log message.

        Returns:
            str: The formatted log message.
        """

        if self.code is not None:
            return '(%s) %s' % (self.code, self.text)
        else:
            return self.text

    def get_level(self) -> int:
        """ Returns the level of the log message.

        Returns:
            int: The level of the log message.
        """

        return self.level

    def __eq__(self, __o: object) -> bool:
        """Compares the log message object with another object for equality.

        Args:
            __o (object): The object to compare with.

        Returns:
            bool: True if the log message objects are equal, False otherwise.
        """

        return self.level == __o.level and self.text == __o.text and self.code == __o.code

class defined_log_messages:
    def __init__(self) -> None:
        self.defined_log_messages = {}
        self.key = '0'

    def add_log_message(self, message, key=None):
        """Add a log message with an optional key. If no key is given, a unique key will be selected automatically.

        Args:
            message (object): The log message to define.
            key (str, optional): The key to associate with the log message. Defaults to None.

        Returns:
            str: The key associated with the defined log message.
        """

        assert isinstance(message, log_message), errors_and_warnings.incorrect_message_datatype()
        if message in self.defined_log_messages.values():
            key = [k for k, v in self.defined_log_messages.items() if v == message]
            return key[0]

        if key is None:
            while self.key in self.defined_log_messages.keys(): self.key = str(int(self.key) + 1)
            key = self.key
        else:
            assert isinstance(key, str), errors_and_warnings.incorrect_key_datatype()
            assert key not in self.defined_log_messages.keys(), errors_and_warnings.defined_key()

        self.defined_log_messages[key] = message
        return key

    def get_defined_log_key(self, message: object) -> str:
        """Returns the key of the given message if already defined.

        Args:
            message (object): The defined log message.

        Returns:
            str: The key associated with the defined log message. None if the message was not defined.
        """

        assert isinstance(message, log_message), errors_and_warnings.incorrect_message_datatype()
        if message in self.defined_log_messages.values():
            key = [k for k, v in self.defined_log_messages.items() if v == message]
            return key[0]
        return None

    def get_defined_log_message(self, key: str) -> str:
        """Returns defined log message related to given key.

        Args:
            key (str): Key of log message.

        Returns:
            str: Log message related to given key.
        """

        assert key in self.defined_log_messages.keys(), errors_and_warnings.undefined_key()
        return self.defined_log_messages[key]

    def delete_defined_log(self, key: object) -> None:
        """Deletes a defined log message.

        Args:
            key (object): The key of the log message to delete.
        """

        assert key in self.defined_log_messages.keys(), errors_and_warnings.undefined_key()
        self.defined_log_messages.pop(key)

class const_log_messages:
    """Contains static methods that return constant messages for logging."""

    @staticmethod
    def get_func_start_message(func_name: str) -> object:
        """Returns a message for logging start of function.

        Args:
            func_name (str): Name of function.

        Returns:
            object: log message object.
        """

        return log_message(level=log_levels.INFO, text='Function {} started'.format(func_name))

    @staticmethod
    def get_func_exception_message(func_name: str) -> object:
        """Returns a message for logging exception of function.

        Args:
            func_name (str): Name of function.

        Returns:
            object: log message object.
        """

        return log_message(level=log_levels.EXCEPTION, text='Function {} exception'.format(func_name))

    @staticmethod
    def get_func_end_message(func_name: str) -> object:
        """Returns a message for logging end of function.

        Args:
            func_name (str): Name of function.

        Returns:
            object: log message object.
        """

        return log_message(level=log_levels.INFO, text='Function {} ended'.format(func_name))

class logger:
    def __init__(
        self, 
        main_folderpath: str,
        date_type: str = date_types.AD_DATE,
        date_format: str = date_formats.YYMMDD,
        time_format: str = time_formats.HHMMSS,
        file_level: int = log_levels.DEBUG,
        console_level: int = log_levels.DEBUG,
        console_print: bool = True,
        current_username: str = "anonymous",
        line_seperator: str = '-',
    ) -> None:
        """Initializes a logger object with the specified configurations.

        Args:
            main_folderpath (str): The main folder path to store log files.
            date_type (str, optional): The type of date format. Defaults to date_types.AD_DATE.
            date_format (str, optional): The format of the date. Defaults to date_formats.YYMMDD.
            time_format (str, optional): The format of the time. Defaults to time_formats.HHMMSS.
            file_level (int, optional): The log level for file logging. Defaults to log_levels.DEBUG.
            console_level (int, optional): The log level for console logging. Defaults to log_levels.DEBUG.
            console_print (bool, optional): Whether to print log messages to the console. Defaults to True.
            current_username (str, optional): The current username for log messages. Defaults to "anonymous".
            line_seperator (str, optional): The separator character for log message lines. Defaults to '-'.
        """
        
        # Create logging object
        self.logger = logging.getLogger("Logger")
        self.logger.setLevel(log_levels.DEBUG)

        # Date
        self.date = date(date_type, date_format)

        # Time
        self.time = time(time_format)

        # Set main folder path
        self.set_main_folderpath(main_folderpath)
        self.set_log_paths()
        self.__create_dailyfolder()

        # Create file handler
        self.file_handler = logging.FileHandler(filename=self.current_filepath, mode='w')
        self.set_file_level(file_level)
        self.file_format = logging.Formatter('%(levelname)s - %(message)s')
        self.file_handler.setFormatter(self.file_format)
        self.logger.addHandler(self.file_handler)

        # Create console handler
        self.console_handler = logging.StreamHandler()
        self.set_console_level(console_level)
        self.console_format = logging.Formatter('%(levelname)s - %(message)s')
        self.console_handler.setFormatter(self.console_format)

        self.set_console_print(console_print)

        # set current username
        self.set_current_user(current_username)

        # set line seperator
        self.set_line_seperator(line_seperator)

        # defined logs 
        self.defined_log_messages = defined_log_messages()

    def set_main_folderpath(self, main_folderpath) -> None:
        """Sets the main folder path for storing log files.

        Args:
            main_folderpath (str): The main folder path to store log files.
        """

        self.main_folderpath = main_folderpath
        self.__create_mainfolder()

        if hasattr(self, 'file_handler'):
            self.__change_path()

    def set_log_paths(self) -> None:
        """Sets the log file paths based on the current date.
        """

        self.daily_folderpath = self.date.get_date_string(sep='-')
        date_time = self.date.get_date_string(sep="-") + "-" + self.time.get_time_string(sep="-")
        self.current_filepath = os.path.join(self.main_folderpath, self.daily_folderpath, date_time+'.log')

    def set_console_print(self, console_print: bool) -> None:
        """Sets whether to print log messages to the console.

        Args:
            console_print (bool): Whether to print log messages to the console.
        """

        self.console_print = console_print
        if self.console_print:
            self.logger.addHandler(self.console_handler)
        else:
            self.logger.removeHandler(self.console_handler)

    def set_file_level(self, level: int) -> None:
        """Sets the log level for file logging. logs with lower level are ignored.

        Args:
            level (int): The log level for file logging.
        """

        levels = [v for k, v in vars(log_levels).items() if not(k.startswith('__'))]
        assert level in levels, errors_and_warnings.undefined_log_level()
        self.file_level = level
        self.file_handler.setLevel(self.file_level)

    def set_console_level(self, level: int) -> None:
        """Sets the log level for console logging. logs with lower level are ignored.

        Args:
            level (int): The log level for console logging.
        """

        levels = [v for k, v in vars(log_levels).items() if not(k.startswith('__'))]
        assert level in levels, errors_and_warnings.undefined_log_level()
        self.console_level = level
        self.console_handler.setLevel(self.console_level)

    def set_current_user(self, current_username: str) -> None:
        """Sets the current username for log messages.

        Args:
            current_username (str): The current username for log messages.
        """

        self.current_username = current_username

    def set_line_seperator(self, sep: str) -> None:
        """Sets the separator character for log message lines.

        Args:
            sep (str): The separator character for log message lines.
        """

        self.line_seperator = sep 

    def function_start_decorator(self, message: object = None) -> None:
        """ Decorator for logging the start of a function.

        Args:
            message (object): The key of defined log message or log message to log at the start of the function.
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not message:
                    msg = const_log_messages.get_func_start_message(func.__name__)
                else:
                    msg = message
                self.create_new_log(message=msg)
                result = func(*args, **kwargs)
                return result
            return wrapper
        return decorator

    def function_exception_decorator(self, message: object = None, with_handling: bool = True) -> None:
        """Decorator for logging exceptions in a function.

        Args:
            message (object, optional): The key of defined log message or log message to log when an exception occurs. Defaults to None.
            with_handling (bool, optional): Whether to handle the exception or re-raise it. Defaults to True.

        Returns:
            None
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    if not message:
                        msg = const_log_messages.get_func_exception_message(func.__name__)
                    else:
                        msg = message
                    self.create_new_log(message=msg)
                    if not with_handling:
                        raise e
            return wrapper
        return decorator

    def function_end_decorator(self, message: object = None) -> None:
        """Decorator for logging the end of a function.

        Args:
            message (object, optional): The key of defined log message to log at the end of the function. Defaults to None.

        Returns:
            None
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                if not message:
                    msg = const_log_messages.get_func_end_message(func.__name__)
                else:
                    msg = message
                self.create_new_log(message=msg)
                return result
            return wrapper
        return decorator

    def create_new_log(self, message: object) -> None:
        """Creates a new log with the specified message.

        Args:
            message (object): The key of defined log message or log message to log.
        """

        assert isinstance(message, str) ^ isinstance(message, log_message), errors_and_warnings.incorrect_input_datatype()
        if isinstance(message, str):
            msg = self.defined_log_messages.get_defined_log_message(message)
        else:
            msg = message

        # get date and time
        date_time = self.date.get_date_string(sep="-") + "-" + self.time.get_time_string(sep="-")

        # change log path on date change
        if self.daily_folderpath != self.date.get_date_string(sep='-'):
            self.__change_path()

        line_seperator = self.line_seperator * 120

        level = msg.get_level()
        msg = msg.get_message()

        # do log by levels
        # debug
        if level == log_levels.DEBUG:
            self.logger.debug(msg='%s - %s : %s\n%s' % (date_time, self.current_username, msg, line_seperator))
        
        # info
        elif level == log_levels.INFO:
            self.logger.info(msg='%s - %s : %s\n%s' % (date_time, self.current_username, msg, line_seperator))
        
        # warning
        elif level == log_levels.WARNING:
            self.logger.warning(msg='%s - %s : %s\n%s' % (date_time, self.current_username, msg, line_seperator))
        
        # error
        elif level == log_levels.ERROR:
            self.logger.error(msg='%s - %s : %s\n%s' % (date_time, self.current_username, msg, line_seperator))
        
        # critical error
        elif level == log_levels.CRITICAL:
            self.logger.critical(msg='%s - %s : %s\n%s' % (date_time, self.current_username, msg, line_seperator))
        
        # exception error (with logging exception message)
        elif level == log_levels.EXCEPTION:
            self.logger.exception(msg='%s - %s : %s\n%s' % (date_time, self.current_username, msg, line_seperator))

    def __change_path(self) -> None:
        """Changes the log file path when the date changes.

        Returns:
            None
        """

        self.set_log_paths()
        self.__create_dailyfolder()

        self.logger.removeHandler(self.file_handler)

        self.file_handler = logging.FileHandler(filename=self.current_filepath, mode='w')
        self.set_file_level(self.file_level)
        self.file_format = logging.Formatter('%(levelname)s - %(message)s')
        self.file_handler.setFormatter(self.file_format)
        self.logger.addHandler(self.file_handler)

    def __create_mainfolder(self) -> None:
        """Creates the main folder for storing log files.

        Returns:
            None
        """

        # create if not exist
        if not os.path.exists(self.main_folderpath):
            os.mkdir(self.main_folderpath)

    def __create_dailyfolder(self) -> None:
        """Creates the daily folder for storing log files.

        Returns:
            None
        """

        # create if not exist
        if not os.path.exists(os.path.join(self.main_folderpath, self.daily_folderpath)):
            os.mkdir(os.path.join(self.main_folderpath, self.daily_folderpath))

