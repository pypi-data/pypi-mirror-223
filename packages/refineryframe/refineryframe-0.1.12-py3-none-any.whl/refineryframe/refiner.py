"""
refineryframe Module

This module provides a Refiner class to encapsulate functions for data refinement
and validation. The Refiner class is designed to work with pandas DataFrames and
perform various checks and replacements for data preprocessing.

Classes:
    Refiner: A class that encapsulates functions for data refinement and validation.

Functions:
    shout(): Print a line of text with a specified length and format.
    get_type_dict_from_dataframe(): Returns a string representation of a dictionary
                                   containing the data types of each column in the given DataFrame.
    set_type_dict(): Change the data types of the columns in the given DataFrame based on a dictionary of intended data types.
    set_types(): Change the data types of the columns in the given DataFrame based on a dictionary of intended data types.
    check_missing_types(): Search for missing types in each column of the DataFrame and log any instances found.
    check_missing_values(): Count the number of NaN, None, and NaT values in each column of a pandas DataFrame.
    check_inf_values(): Count the inf values in each column of a pandas DataFrame.
    check_date_format(): Check if the values in the datetime columns of the input dataframe
                            have the expected 'YYYY-MM-DD' format.
    check_duplicates(): Check for duplicates in a pandas DataFrame.
    check_col_names_types(): Check if a given dataframe has the same column names as keys in a given dictionary
                                and those columns have the same types as items in the dictionary.
    check_numeric_range(): Check if numeric values are in expected ranges.
    check_date_range(): Check if dates are in expected ranges.
    detect_unexpected_values(): Detect unexpected values in a pandas DataFrame.
    replace_unexpected_values(): Replace unexpected values in a pandas DataFrame with missing types.

Constants:
    MISSING_TYPES: A dictionary containing default missing data types.
"""

import logging
import pandas as pd
import attr
from refineryframe.other import shoutOUT, get_type_dict, set_types
from refineryframe.detect_unexpected import check_date_range, \
    check_col_names_types, check_date_format, check_duplicates, \
        check_inf_values, check_missing_values, check_numeric_range, \
            check_missing_types, detect_unexpected_values
from refineryframe.replace_unexpected import replace_unexpected_values

@attr.s
class Refiner:

    """
    Refiner is a class that encapsulates funtions from refineframe.
    """


    # inputs
    dataframe = attr.ib(type=pd.DataFrame)
    replace_dict = attr.ib(default=None, type=dict)

    # inputs with defaults
    MISSING_TYPES = attr.ib(default={'date_not_delivered': '1850-01-09',
                 'numeric_not_delivered': -999,
                 'character_not_delivered': 'missing'}, type=dict)
    expected_date_format = attr.ib(default='%Y-%m-%d', type=str)
    mess = attr.ib(default="INITIAL PREPROCESSING", type=str)
    shout_type = attr.ib(default="HEAD2", type=str)

    logger = attr.ib(default=logging)
    logger_name = attr.ib(default='Refiner')
    loggerLvl = attr.ib(default=logging.INFO)
    dotline_length = attr.ib(default=50, type=int)

    lower_bound = attr.ib(default=-float("inf"))
    upper_bound = attr.ib(default=float("inf"))
    earliest_date = attr.ib(default="1900-08-25")
    latest_date = attr.ib(default="2100-01-01")

    unexpected_exceptions_duv = attr.ib(default={"col_names_types": "NONE",
                                              "missing_values": "NONE",
                                              "missing_types": "NONE",
                                              "inf_values": "NONE",
                                              "date_format": "NONE",
                                              "duplicates": "NONE",
                                              "date_range": "NONE",
                                              "numeric_range": "NONE"}, type=dict)

    unexpected_exceptions_ruv = attr.ib(default={"irregular_values": "NONE",
                                                      "date_range": "NONE",
                                                      "numeric_range": "NONE",
                                                      "capitalization": "NONE",
                                                      "unicode_character": "NONE"}, type=dict)

    unexpected_conditions = attr.ib(default=None)

    ignore_values = attr.ib(default=[])
    ignore_dates = attr.ib(default=[])

    # outputs
    type_dict = attr.ib(default={}, init = False, type=dict)

    MISSING_TYPES_TEST = attr.ib(default=None, init = False)
    MISSING_COUNT_TEST = attr.ib(default=None, init = False)
    NUM_INF_TEST = attr.ib(default=None, init = False)
    DATE_FORMAT_TEST = attr.ib(default=None, init = False)
    DATE_RANGE_TEST = attr.ib(default=None, init = False)
    DUPLICATES_TEST = attr.ib(default=None, init = False)
    COL_NAMES_TYPES_TEST = attr.ib(default=None, init = False)
    NUMERIC_RANGE_TEST = attr.ib(default=None, init = False)

    duv_score = attr.ib(default=None, init = False)
    ruv_score0 = attr.ib(default=None, init = False)
    ruv_score1 = attr.ib(default=None, init = False)
    ruv_score2 = attr.ib(default=None, init = False)

    def __attrs_post_init__(self):
        self.initialize_logger()

    def initialize_logger(self):

        """
        Initialize a logger for the class instance based on the specified logging level and logger name.
        """

        logging.basicConfig(level=self.loggerLvl)
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.loggerLvl)

        self.logger = logger


    def shout(self):

        """
        Print a line of text with a specified length and format.
        """

        shoutOUT(output_type=self.shout_type,
                 mess=self.mess,
                 dotline_length=self.dotline_length,
                 logger=self.logger)

    def get_type_dict_from_dataframe(self,
                      explicit=True,
                      stringout=False):

        """
        Returns a string representation of a dictionary containing the data types
        of each column in the given pandas DataFrame.

        Numeric columns will have type 'numeric', date columns will have type 'date',
        character columns will have type 'category', and columns containing 'id' at
        the beginning or end of their name will have type 'index'.
        """

        type_dict = get_type_dict(dataframe=self.dataframe,
                                       explicit=explicit,
                                       stringout=stringout)

        return type_dict

    def set_type_dict(self,
                      type_dict=None,
                      explicit=True,
                      stringout=False):

        """
        Change the data types of the columns in the given DataFrame
        based on a dictionary of intended data types.
        """

        if type_dict is None:
            type_dict = get_type_dict(dataframe=self.dataframe,
                                       explicit=explicit,
                                       stringout=stringout,
                                      logger = self.logger)

        self.type_dict = type_dict


    def set_types(self,
                  type_dict=None,
                  replace_dict=None,
                  expected_date_format=None):

        """
        Change the data types of the columns in the given DataFrame
        based on a dictionary of intended data types.
        """

        if type_dict is None:
            type_dict = self.type_dict
        if replace_dict is None:
            replace_dict = self.replace_dict
        if expected_date_format is None:
            expected_date_format = self.expected_date_format

        self.dataframe = set_types(dataframe=self.dataframe,
                                  types_dict_str=type_dict,
                                  replace_dict=replace_dict,
                                  expected_date_format=expected_date_format,
                                      logger = self.logger)

    def check_missing_types(self):

        """
        The function takes a DataFrame and a dictionary of missing types as input, and
        searches for any instances of these missing types in each column of the DataFrame.
        If any instances are found, a warning message is logged containing the column name,
        the missing value, and the count of missing values found.
        """

        self.MISSING_TYPES_TEST = check_missing_types(dataframe = self.dataframe,
                                                        MISSING_TYPES = self.MISSING_TYPES,
                                                        independent = True,
                                      logger = self.logger)

    def check_missing_values(self):

        """
        Count the number of NaN, None, and NaT values in each column of a pandas DataFrame.
        """

        self.MISSING_COUNT_TEST = check_missing_values(dataframe = self.dataframe,
                                      logger = self.logger)

    def check_inf_values(self):

        """
        Count the inf values in each column of a pandas DataFrame.
        """

        self.NUM_INF_TEST = check_inf_values(dataframe = self.dataframe,
                                             independent = True,
                                             logger = self.logger)

    def check_date_format(self):

        """
        Check if the values in the datetime columns of the input dataframe
        have the expected 'YYYY-MM-DD' format.
        """

        self.DATE_FORMAT_TEST = check_date_format(dataframe = self.dataframe,
                                                  expected_date_format = self.expected_date_format,
                                                  independent = True,
                                                  logger = self.logger)

    def check_duplicates(self,
                         subset = None):

        """
        Check for duplicates in a pandas DataFrame.
        """

        self.DUPLICATES_TEST = check_duplicates(dataframe = self.dataframe,
                                                 subset = subset,
                                                 independent = True,
                                                 logger = self.logger)

    def check_col_names_types(self):

        """
        Checks if a given dataframe has the same column names as keys in a given dictionary
        and those columns have the same types as items in the dictionary.
        """

        self.COL_NAMES_TYPES_TEST = check_col_names_types(dataframe = self.dataframe,
                          types_dict_str = self.type_dict,
                          independent = True,
                                      logger = self.logger)

    def check_numeric_range(self,
                            numeric_cols = None,
                            lower_bound = None,
                            upper_bound = None,
                            ignore_values = None):

        """
        Check if numeric values are in expected ranges
        """

        if lower_bound is None:
            lower_bound = self.lower_bound
        if upper_bound is None:
            upper_bound = self.upper_bound
        if ignore_values is None:
            ignore_values = self.ignore_values

        self.NUMERIC_RANGE_TEST = check_numeric_range(dataframe = self.dataframe,
                                                      numeric_cols = numeric_cols,
                                                      lower_bound = lower_bound,
                                                      upper_bound = upper_bound,
                                                      independent = True,
                                                      ignore_values = ignore_values,
                                                      logger = self.logger)

    def check_date_range(self,
                        earliest_date = None,
                        latest_date = None,
                        ignore_dates = None):

        """
        Check if dates are in expected ranges
        """

        if earliest_date is None:
            earliest_date = self.earliest_date
        if latest_date is None:
            latest_date = self.latest_date
        if ignore_dates is None:
            ignore_dates = self.ignore_dates

        self.DATE_RANGE_TEST = check_date_range(dataframe = self.dataframe,
                                                 earliest_date = earliest_date,
                                                 latest_date = latest_date,
                                                 independent = True,
                                                 ignore_dates = ignore_dates,
                                                logger = self.logger)

    def detect_unexpected_values(self,
                                 MISSING_TYPES = None,
                                 unexpected_exceptions = None,
                                 unexpected_conditions = None,
                                 ids_for_dup = None,
                                 TEST_DUV_FLAGS_PATH = None,
                                 types_dict_str = None,
                                 expected_date_format = None,
                                 earliest_date = None,
                                 latest_date = None,
                                 numeric_lower_bound = None,
                                 numeric_upper_bound = None,
                                 print_score = True):

        """
        Detect unexpected values in a pandas DataFrame.
        """

        if MISSING_TYPES is None:
            MISSING_TYPES = self.MISSING_TYPES
        if unexpected_exceptions is None:
            unexpected_exceptions = self.unexpected_exceptions_duv
        if unexpected_conditions is None:
            unexpected_conditions = self.unexpected_conditions
        if types_dict_str is None:
            types_dict_str = self.type_dict
        if expected_date_format is None:
            expected_date_format = self.expected_date_format
        if earliest_date is None:
            earliest_date = self.earliest_date
        if latest_date is None:
            latest_date = self.latest_date
        if numeric_lower_bound is None:
            numeric_lower_bound = self.lower_bound
        if numeric_upper_bound is None:
            numeric_upper_bound = self.upper_bound

        self.duv_score = detect_unexpected_values(dataframe = self.dataframe,
                                                 MISSING_TYPES = MISSING_TYPES,
                                                 unexpected_exceptions = unexpected_exceptions,
                                                 unexpected_conditions = unexpected_conditions,
                                                 ids_for_dup = ids_for_dup,
                                                 TEST_DUV_FLAGS_PATH = TEST_DUV_FLAGS_PATH,
                                                 types_dict_str = types_dict_str,
                                                 expected_date_format = expected_date_format,
                                                 earliest_date = earliest_date,
                                                 latest_date = latest_date,
                                                 numeric_lower_bound = numeric_lower_bound,
                                                 numeric_upper_bound = numeric_upper_bound,
                                                 print_score = print_score,
                                      logger = self.logger)

    def replace_unexpected_values(self,
                             MISSING_TYPES = None,
                             unexpected_exceptions = None,
                             unexpected_conditions = None,
                             TEST_RUV_FLAGS_PATH = None,
                             earliest_date = None,
                             latest_date = None,
                             numeric_lower_bound = None,
                             numeric_upper_bound = None):

        """
        Replace unexpected values in a pandas DataFrame with missing types.
        """

        if MISSING_TYPES is None:
            MISSING_TYPES = self.MISSING_TYPES
        if unexpected_exceptions is None:
            unexpected_exceptions = self.unexpected_exceptions_ruv
        if unexpected_conditions is None:
            unexpected_conditions = self.unexpected_conditions
        if earliest_date is None:
            earliest_date = self.earliest_date
        if latest_date is None:
            latest_date = self.latest_date
        if numeric_lower_bound is None:
            numeric_lower_bound = self.lower_bound
        if numeric_upper_bound is None:
            numeric_upper_bound = self.upper_bound

        out_dict = replace_unexpected_values(dataframe = self.dataframe,
                             MISSING_TYPES = MISSING_TYPES,
                             unexpected_exceptions = unexpected_exceptions,
                             unexpected_conditions = unexpected_conditions,
                             TEST_RUV_FLAGS_PATH = TEST_RUV_FLAGS_PATH,
                             earliest_date = earliest_date,
                             latest_date = latest_date,
                             numeric_lower_bound = numeric_lower_bound,
                             numeric_upper_bound = numeric_upper_bound,
                                      logger = self.logger)

        self.dataframe = out_dict['dataframe']
        self.ruv_score0 = out_dict['ruv_score0']
        self.ruv_score1 = out_dict['ruv_score1']
        self.ruv_score2 = out_dict['ruv_score2']
