from python_helper import DateTimeHelper, StringHelper, Constant, ObjectHelper, log

from decimal import Decimal

try:
    from pyspark.sql.dataframe import DataFrame
    from pyspark.sql import SparkSession
except Exception as exception:
    print(exception)
    DataFrame = None
    SparkSession = None

try:
    from pyspark.sql.functions import col as spark_col
    from pyspark.sql.functions import sum as spark_sum
    from pyspark.sql.functions import round as spark_round
except Exception as exception:
    print(exception)
    spark_col, spark_sum, spark_round = (
        None, 
        None, 
        None
    )

try:
    from pyspark.sql.types import StructType, StructField, StringType, DoubleType, DecimalType, IntegerType, DateType, TimestampType
except Exception as exception:
    print(exception)
    StructType, StructField, StringType, DoubleType, DecimalType, IntegerType, DateType, TimestampType = (
        None, 
        None, 
        None, 
        None, 
        None, 
        None, 
        None, 
        None
    )


DB_SPARK_SESSION_KEY = 'DB_SPARK_SESSION'
DB_SPARK_DF_DISPLAY_KEY = 'DB_SPARK_DF_DISPLAY'
GLOBAL_VALUES = {
    DB_SPARK_SESSION_KEY: None,
    DB_SPARK_DF_DISPLAY_KEY: None
}

# # global DB_SPARK_SESSION
# DB_SPARK_SESSION = None

# # global DB_SPARK_DF_DISPLAY
# DB_SPARK_DF_DISPLAY = None


spark_col = spark_col
spark_sum = spark_sum
spark_round = spark_round
StructType = StructType
StructField = StructField
StringType = StringType
DoubleType = DoubleType
DecimalType = DecimalType
IntegerType = IntegerType
DateType = DateType
TimestampType = TimestampType
Decimal = Decimal

DataFrame = DataFrame
SparkSession = SparkSession


def set_default_spark_session(spark_session):
    # global DB_SPARK_SESSION
    # DB_SPARK_SESSION = spark_session
    GLOBAL_VALUES[DB_SPARK_SESSION_KEY] = spark_session


def set_default_display_spark_dataframe(spark_df_display):
    # global DB_SPARK_DF_DISPLAY
    # DB_SPARK_DF_DISPLAY = spark_df_display
    GLOBAL_VALUES[DB_SPARK_DF_DISPLAY_KEY] = spark_df_display


try:
    set_default_spark_session(spark)
except Exception as exception:
    print('Default "spark" session not loaded. Please run:          set_default_spark_session(spark)')


try :
    set_default_display_spark_dataframe(display)
except Exception as exception:
    print('Default "display" function not loaded. Please run:       set_default_display_spark_dataframe(display)')


def get_spark_session(spark_session: SparkSession = None) -> SparkSession: 
    if ObjectHelper.isNotNone(spark_session):
        return spark_session
    try:
        # global DB_SPARK_SESSION
        # return DB_SPARK_SESSION
        return GLOBAL_VALUES[DB_SPARK_SESSION_KEY]
    except Exception as exception:
        print(exception)
        print(f'''databricks_helper.DB_SPARK_SESSION = spark''')
    return None


def get_display_spark_dataframe_caller(spark_df_display = None):
    if ObjectHelper.isNotNone(spark_df_display):
        return spark_df_display
    try:
        # global DB_SPARK_DF_DISPLAY
        # return DB_SPARK_DF_DISPLAY
        return GLOBAL_VALUES[DB_SPARK_DF_DISPLAY_KEY]
    except Exception as exception:
        print(exception)
        print(f'''databricks_helper.DB_SPARK_DF_DISPLAY = display''')
    return None


def two_digits_prefixed_with_zeros_as_string(day_as_int):
    return f'{day_as_int:0>2}'



ONE_MILION = 1000000
VERY_LOW_DECIMAL_VALUE = 1 / (100 * ONE_MILION)

NULL_QUERY = 'null'

FIRST_MONTH_DAY = 1
MINIMUM_LAST_MONTH_DAY = 28
FIRST_MONTH_DAY_AS_STRING = two_digits_prefixed_with_zeros_as_string(FIRST_MONTH_DAY) ###- '01'
MINIMUM_LAST_MONTH_DAY_AS_STRING = two_digits_prefixed_with_zeros_as_string(MINIMUM_LAST_MONTH_DAY) ###- '28'


def build_first_month_date_given_date_as_string_list(given_date_as_string_list):
    return DateTimeHelper.dateOf(
        DateTimeHelper.of(
            f'''{
                given_date_as_string_list[0]
            }{Constant.DASH}{
                given_date_as_string_list[1]
            }{Constant.DASH}{FIRST_MONTH_DAY_AS_STRING}{Constant.SPACE}{
                DateTimeHelper.DEFAULT_TIME_BEGIN
            }'''
        )
    )


def get_first_month_date(given_date):
    given_date_as_string_list = str(given_date).split(Constant.DASH)
    return build_first_month_date_given_date_as_string_list(given_date_as_string_list)


def get_last_month_date(given_date):
    return DateTimeHelper.dateOf(
        DateTimeHelper.minusDays(
            DateTimeHelper.plusMonths(
                DateTimeHelper.of(date=f'{get_first_month_date(given_date)}'),
                months=1
            ),
            days=1
        )
    )


def get_last_month_day(given_datetime):
    return int(str(get_last_month_date(given_datetime)).split(Constant.DASH)[-1])


def get_year_dash_month(given_datetime):
    # The idea here is to extract year:
    # Example: 2023-05-12 -> 2023-05
    return StringHelper.join(
        str(given_datetime).split(Constant.DASH)[:-1],
        character = Constant.DASH
    )


def get_year(given_date):
    # The idea here is to extract year:
    # Example: 2023-05-12 -> 2023
    return str(given_date).split(Constant.DASH)[0]


def get_month(given_date):
    # The idea here is to extract month from a date:
    # Example: 2023-05-12 -> 05
    return str(given_date).split(Constant.DASH)[1]


def get_month_dash_day(given_date):
    # The idea here is to extract month dash day from a date:
    # Example: 2023-05-12 -> 05-12
    return StringHelper.join(
        str(given_date).split(Constant.DASH)[-2:],
        character = Constant.DASH
    )


def remove_leading_zeros(integer_as_string):
    while integer_as_string.startswith('0') and 1 < len(integer_as_string):
        integer_as_string = integer_as_string[1:]
    return integer_as_string


def get_distinct_and_ordered(given_list):
    return ObjectHelper.deepSort(list(set(given_list)))


def query_value_as_string_is_not_null(query_value_as_string) -> bool:
    return (
        not query_value_as_string == NULL_QUERY and 
        query_value_as_string is not None
    )


def get_query_value_or_null(given_query_value: str) -> str:
    return given_query_value if ObjectHelper.isNotNone(given_query_value) else NULL_QUERY


def print_attribute(attribute_name, attribute_value):
    print(f'''{attribute_name}: {attribute_value}''')


def get_monetary_decimal_type() -> DecimalType:
    return DecimalType(32, 2)


def get_percentual_decimal_type() -> DecimalType:
    return DecimalType(32, 4)


def to_monetary_decimal(float_value: float) -> Decimal:
    return Decimal(float_value).quantize(Decimal('.01'))
                                         

def to_percentual_decimal(float_value: float) -> Decimal:
    return Decimal(float_value).quantize(Decimal('.0001'))


def parse_column_name(column_name: str) -> str:
    parsed_column_name = column_name.lower()
    parsed_column_name = parsed_column_name.replace('(-)', 'menos').replace(' ', '_').replace('-', '_')
    parsed_column_name = parsed_column_name.replace('%', 'percentual')
    for character_set in [Constant.A, Constant.E, Constant.I, Constant.O, Constant.U]:
        character_list = list(character_set)
        for character in character_list:
            parsed_column_name = parsed_column_name.replace(
                character, 
                'a' 
                if 'á' in character_list else 'e' 
                if 'é' in character_list else 'i' 
                if 'í' in character_list else 'o' 
                if 'ó' in character_list else 'u' 
                if 'ú' in character_list else character
            )
    parsed_column_name = parsed_column_name.replace('_da_', '_')
    parsed_column_name = parsed_column_name.replace('_de_', '_')
    parsed_column_name = parsed_column_name.replace('_do_', '_')
    return parsed_column_name


def wrap_column_name(column_name: str) -> str:
    return f'`{column_name}`'


def to_query_string_value(value) -> str:
    return value if str(value).startswith(Constant.SINGLE_QUOTE) else f'{Constant.SINGLE_QUOTE}{value}{Constant.SINGLE_QUOTE}'


def date_to_query_date(given_date):
    return to_query_string_value(given_date) 


def build_month_dash_day_query_from_date(given_date):
    # The idea here is to extract month dash day from a date for queries:
    # Example: 2023-05-14 -> '05-14'
    return StringHelper.join(
        [
            Constant.SINGLE_QUOTE,
            get_month_dash_day(given_date),
            Constant.SINGLE_QUOTE
        ]
    )

def is_empty_query(column_name):
    return f'''({replace_if_empty_query(column_name, NULL_QUERY)} IS {NULL_QUERY})'''


def is_not_empty_query(column_name):
    return f'''NOT {is_empty_query(column_name)}'''


def query_command_over_columns(*column_names, command=None):
    return StringHelper.join(
        [
            command,
            StringHelper.join([*column_names], character=Constant.COMA_SPACE)
        ], 
        character=Constant.SPACE
    )


def query_order_by(*column_names):
    return query_command_over_columns(*column_names, command='ORDER BY')


def query_group_by(*column_names):
    return query_command_over_columns(*column_names, command='GROUP BY')
    

def query_replace(column_name_or_value, old_substring, new_substring):
    return f'''REPLACE({column_name_or_value}, {old_substring}, {new_substring})'''


def get_only_numbers_query(collumn_name_or_string):
    return f'''regexp_extract({collumn_name_or_string}, '\\\\d+', 0)'''


def remove_characters_query(collumn_name_or_string, *characters):
    return f'''regexp_replace({collumn_name_or_string}, '[{StringHelper.join([*characters])}]', '')'''

    
def get_distinct_collection_from_table(table_name, column_name):
    return spark_sql(f'''
        SELECT
            collect_set(tbl.{column_name}) AS collection_set
        FROM {table_name} tbl
    ''')


def parse_dt_query(date_column_name):
    return f'SUBSTRING({cast_to_query_string(date_column_name, 10)}, 0, 10)'


def build_month_dash_day_query(date_column_name):
    # The idea here is to extract month dash day from a date:
    # Example: 2023-05-14 -> 05-14
    return f'SUBSTRING({cast_to_query_string(date_column_name, 10)}, 6, 5)'


def build_month_query(date_column_name):
    # The idea here is to extract month from a date:
    # Example: 2023-05-14 -> 05
    return f'SUBSTRING({cast_to_query_string(date_column_name, 10)}, 6, 2)'


def build_year_dash_month(date_column_name):
    # The idea here is to extract month dash day from a date:
    # Example: 2023-05-14 -> 05-14
    return f'SUBSTRING({cast_to_query_string(date_column_name, 10)}, 1, 7)'


def list_to_query_in_integer_list(given_list):
    return StringHelper.join(
        [
            Constant.OPEN_TUPLE,
            StringHelper.join([str(element) for element in given_list], character = Constant.COMA),
            Constant.CLOSE_TUPLE
        ],
        character = Constant.BLANK
    )


def list_to_query_in_string_list(given_list):
    return list_to_query_in_integer_list([
        f'{Constant.SINGLE_QUOTE}{i}{Constant.SINGLE_QUOTE}'
        for i in given_list
    ])


def cast_to_query_string(column_name, size):
    return f'CAST({column_name} AS VARCHAR({size}))'


def replace_if_empty_query(column_name, defautl_value):
    return f'''nvl(NULLIF({column_name},''), {defautl_value})'''


def cast_to_query_2_digits_decimal(given_query):
    return f'CAST(({given_query}) AS DECIMAL(32,2))'


def cast_to_query_percentual_decimal(given_query):
    return cast_to_query_2_digits_decimal(f'''100.0 * {replace_if_empty_query(given_query, '0')}''')


def cast_to_query_monetary_decimal(given_query):
    return cast_to_query_2_digits_decimal(given_query)


def cast_to_query_integer(given_query):
    return f'CAST({given_query} AS INT)'


def cast_to_query_big_integer(column_name):
    return f'''CAST({column_name} AS BIGINT)'''


def concat_query(*args, separator=Constant.BLANK):
    return f'''concat_ws('{separator}', {StringHelper.join(
        [
            arg
            for arg in args
        ],
        character = Constant.COMA_SPACE
    )})'''


def concat_dash_query(*args):
    return concat_query(*args, separator=Constant.DASH)
    

def concat_query_date(year_column_name_or_value, month_column_name_or_value, day_column_name_or_value):
    return concat_dash_query(
        cast_to_query_integer(year_column_name_or_value),
        f'''lpad({cast_to_query_integer(month_column_name_or_value)}, 2, {to_query_string_value('0')})''',
        f'''lpad({cast_to_query_integer(day_column_name_or_value)}, 2, {to_query_string_value('0')})'''
    )


def get_distinct_integer_collection_from_table(table_name, column_name):
    try:
        return get_distinct_and_ordered([
            int(cd_as_string)
            for cd_as_string in spark_sql(f'''
                SELECT
                    collect_set({cast_to_query_integer(f'tbl.{column_name}')}) AS {column_name}_set
                FROM {table_name} tbl
                '''
                # , show_query=False, show_dataframe=False
            ).select(f'{column_name}_set').first()[0]
            if query_value_as_string_is_not_null(cd_as_string)
        ])
    except Exception as exception:
        log.failure(get_distinct_integer_collection_from_table, 'Not possible to extract collection. Returning empty collection by default', exception=exception, muteStackTrace=True)
        return []
    

def get_distinct_integer_collection_from_table_by_cd(integer_cd, table_name, cd_column_name, column_name):
    try:
        return get_distinct_and_ordered([
            int(cd_as_string)
            for cd_as_string in spark_sql(f'''
                SELECT
                    collect_set({cast_to_query_integer(f'tbl.{column_name}')}) AS {column_name}_set
                FROM {table_name} tbl
                WHERE (
                    {cast_to_query_integer(f'tbl.{cd_column_name}')} = {cast_to_query_integer(integer_cd)}
                    AND NOT {replace_if_empty_query(f'tbl.{column_name}', NULL_QUERY)} IS {NULL_QUERY}
                )
                '''
                # , show_query=False, show_dataframe=False
            ).select(f'{column_name}_set').first()[0]
            if query_value_as_string_is_not_null(cd_as_string)
        ])
    except Exception as exception:
        log.failure(get_distinct_integer_collection_from_table_by_cd, 'Not possible to extract collection. Returning empty collection by default', exception=exception, muteStackTrace=True)
        return []


def query_distinct_collection(column_name: str, view_or_table_name: str, condition='1=1', by_column_name=None, by_column_value=None) -> DataFrame:
    return spark_sql(f'''
        SELECT DISTINCT {column_name} 
        FROM {view_or_table_name} 
        WHERE {
            condition if ObjectHelper.isNoneOrBlank(by_column_name) else f'({by_column_name} = f"{NULL_QUERY if ObjectHelper.isNone(by_column_value) else by_column_value}")'
        } 
        ORDER BY {column_name}
    ''')  


def display_spark_dataframe(spark_df: DataFrame, *args, spark_df_display=None, **kwargs) -> DataFrame:
    ###- Here, display() is a builting function in databricks
    get_display_spark_dataframe_caller(spark_df_display=spark_df_display)(spark_df, *args, **kwargs)
    return spark_df


def display_query(givenQuery: str, show_query=True) -> str:
    if show_query:
        print(givenQuery)
    return givenQuery


def spark_sql(*agrs, show_dataframe=True, spark_session: SparkSession = None, spark_df_display=None, **kwargs) -> DataFrame:
    df = get_spark_session(spark_session=spark_session).sql(display_query(*agrs, **kwargs))
    if show_dataframe:
        display_spark_dataframe(df, spark_df_display=spark_df_display)
    return df


def spark_create_or_replace_temp_view_from_sql(*agrs, view_name=None, **kwargs) -> DataFrame:
    df = spark_sql(*agrs, **kwargs)
    df.createOrReplaceTempView(view_name)
    return df


def spark_big_sql(*agrs, spark_sql_caller=spark_sql, **kwargs):
    df = spark_sql_caller(*agrs, **kwargs)
    print(f'Rows count: {df.count()}')
    return df


def spark_create_or_replace_temp_view_from_big_sql(*agrs, **kwargs) -> DataFrame:
    return spark_big_sql(*agrs, spark_sql_caller=spark_create_or_replace_temp_view_from_sql, **kwargs)
    

def spark_createDataFrame(*agrs, show_dataframe=True, order_by=None, spark_session: SparkSession = None, spark_df_display=None, **kwargs) -> DataFrame:
    df = get_spark_session(spark_session=spark_session).createDataFrame(*agrs, **kwargs)
    if ObjectHelper.isNotEmpty(order_by):
        df = df.orderBy(*order_by)
    if show_dataframe:
        display_spark_dataframe(df, spark_df_display=spark_df_display)
    return df


def override_table_and_schema(spark_df, table_name):
    return save_as_table(to_spark_df_override_delta_mode(spark_df).option('overwriteSchema', 'true'), table_name)


def override_table(spark_df, table_name):
    return save_as_table(to_spark_df_override_delta_mode(spark_df), table_name)


def to_spark_df_override_delta_mode(spark_df):
    if 0 >= spark_df.count():
        raise Exception('spark dataframe cannot be empty')
    return spark_df.write.format('delta').mode('overwrite')


def save_as_table(spark_df_override_delta_mode, table_name):
    return spark_df_override_delta_mode.saveAsTable(table_name)


