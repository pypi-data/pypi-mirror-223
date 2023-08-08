import argparse
import mysql.connector
from clickhouse_driver import Client
from odps import ODPS, errors
import logging
import json
import os
import time

# Database configurations, modify according to your actual settings
mysql_host = "rm-uf698x9pde1ytqxe8ko.mysql.rds.aliyuncs.com"
mysql_port = "3306"
mysql_user = "nl_bi"
mysql_passwd = "nenglianginfo_2023"

clickhouse_host = "cc-uf651o30oz76wz9p9.public.clickhouse.ads.aliyuncs.com"
clickhouse_port = "9000"
clickhouse_user = "nl2020"
clickhouse_passwd = "nengliang2020!"

odps_access_id = "LTAI5tSnVoE2dHf5MakuEZ2z"
odps_access_key = "oZKfxkOiMfhB5xsCoEpDhIqmoibhbm"
odps_project = "prj_yingshou_20230629"
odps_endpoint = "http://service.cn-shanghai.maxcompute.aliyun.com/api"

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_connection(db_type, database=None):
    if db_type == "mysql":
        if database is None:
            raise ValueError("Database name must be provided for MySQL.")
        return mysql.connector.connect(host=mysql_host, port=mysql_port, user=mysql_user, password=mysql_passwd,
                                       database=database)
    elif db_type == "clickhouse":
        try:
            logging.info(f"Connecting to ClickHouse: {clickhouse_host}:{clickhouse_port}")
            return Client(host=clickhouse_host, port=clickhouse_port, user=clickhouse_user, password=clickhouse_passwd,
                          database=database)
        except Exception as e:
            logging.error(f"Failed to connect to ClickHouse: {str(e)}")
            raise e

    elif db_type == "maxcompute":
        return ODPS(odps_access_id, odps_access_key, odps_project, endpoint=odps_endpoint)
    else:
        raise ValueError("Unsupported database type.")


def get_columns(db_type, database, table):
    connection = None
    cursor = None
    try:
        if db_type == "mysql":
            connection = get_connection(db_type, database)
            cursor = connection.cursor()
            # Use the DESC statement to get column information
            sql = "DESC {}.{}".format(database, table)
            cursor.execute(sql)
            columns_data = cursor.fetchall()
            # Extract column names and data types simultaneously
            column_info = [(col_data[0], col_data[1].decode('utf-8')) for col_data in columns_data]
            return column_info

        elif db_type == "clickhouse":
            connection = get_connection(db_type, database='bi_report')
            # Use the DESCRIBE TABLE statement to get column information
            sql = "DESCRIBE TABLE {}.{}".format(database, table)
            result = connection.execute(sql)
            # Extract column names and data types simultaneously
            column_info = [(col_data[0], col_data[1]) for col_data in result]
            return column_info

        elif db_type == "maxcompute":
            connection = get_connection(db_type)
            table_obj = connection.get_table(f"{database}.{table}")
            column_info = [(column.name, column.type.name) for column in table_obj.table_schema.columns]
            return column_info

        else:
            raise ValueError("Unsupported database type: {}".format(db_type))

    finally:
        # Close the connection properly for MySQL and ClickHouse
        if db_type == "mysql":
            cursor.close()
            connection.close()


def map_columns(column_info, source_db_type, target_db_type):
    mapped_columns = []
    for col_name, col_type in column_info:
        # Mapping rules for MYSQL->MaxCompute
        if source_db_type == "mysql" and target_db_type == "maxcompute":
            if any(keyword in col_type for keyword in ['char', 'time', 'date']):
                col_type = "string"
            elif any(keyword in col_type for keyword in ['int']):
                col_type = "bigint"
            elif any(keyword in col_type for keyword in ['decimal', 'float', 'double']):
                col_type = "double"
            else:
                col_type = "string"
        # Mapping rules for Maxcompute->Mysql
        elif source_db_type == "maxcompute" and target_db_type == "mysql":
            if any(keyword in col_type for keyword in ['string', 'date', 'time', 'bool']):
                col_type = "varchar(255)"
            elif any(keyword in col_type for keyword in ['int']):
                col_type = "bigint"
            elif any(keyword in col_type for keyword in ['decimal', 'float', 'double']):
                col_type = "double"
            else:
                col_type = "varchar(255)"
        # Mapping rules for Maxcompute->ClickHouse
        elif source_db_type == "maxcompute" and target_db_type == "clickhouse":
            if any(keyword in col_type for keyword in ['string', 'date', 'time', 'bool']):
                col_type = "String"
            elif any(keyword in col_type for keyword in ['int']):
                col_type = "Int64"
            elif any(keyword in col_type for keyword in ['decimal', 'float', 'double']):
                col_type = "Float64"
            else:
                col_type = "String"

        # Mapping rules for MySQL->Clickhouse
        elif source_db_type == "mysql" and target_db_type == "clickhouse":
            if any(keyword in col_type for keyword in ['char', 'date', 'time', 'bool']):
                col_type = "String"
            elif any(keyword in col_type for keyword in ['int']):
                col_type = "Int64"
            elif any(keyword in col_type for keyword in ['decimal', 'float', 'double']):
                col_type = "Float64"
            else:
                col_type = "String"

        else:
            raise ValueError("Unsupported source or target database type.")

        # Append the mapped column information
        mapped_columns.append((col_name, col_type))
    logger.info(f"Merged structure for {args.targetdb}.{args.targettable}:")
    merged_structure = [(col[0], col[1], gen_col[1]) for col, gen_col in zip(column_info, mapped_columns)]
    logger.info(merged_structure)
    return mapped_columns


def create_table_mysql(target_db, target_table, map_column_info):
    # Extract the column name and type from each tuple and join them into a comma-separated string
    column_definitions = [f"{col_info[0]} {col_info[1]}" for col_info in map_column_info]

    create_table_sql = "CREATE TABLE {}.{} (\n    {}\n)".format(target_db, target_table,
                                                                ',\n    '.join(column_definitions))

    connection = get_connection("mysql", database=target_db)
    cursor = connection.cursor()

    try:
        # Check if the table exists
        cursor.execute(
            f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{target_db}' AND TABLE_NAME = '{target_table}'")
        if cursor.fetchone()[0] > 0:

            logger.info(f"Table {target_db}.{target_table} already exists.")
            orig_columns = get_columns("mysql", target_db, target_table)

            if orig_columns == map_column_info:
                # Table exists with the same columns and types, no need to recreate
                logger.info(
                    f"Table {target_db}.{target_table} already exists with the same columns and types. Skipping table creation.")
            else:
                logger.info(
                    f"Table {target_db}.{target_table} already exists but have different columns and types,so drop table {target_db}.{target_table}...")
                # Table exists with different columns or types, drop it
                cursor.execute(f"DROP TABLE {target_db}.{target_table}")
                # Execute the CREATE TABLE SQL statement
                logger.info(f"Executing SQL to create table {target_db}.{target_table}:")
                logger.info(f"Table {target_db}.{target_table} created by:{create_table_sql}")
                cursor.execute(create_table_sql)
                logger.info(f"Table {target_db}.{target_table} created successfully.")
    except Exception as e:
        logger.error(f"Failed to create table {target_db}.{target_table}: {str(e)}")
    finally:
        cursor.close()
        connection.close()


def create_table_clickhouse(target_db, target_table, map_column_info):
    # Extract the column name and type from each tuple and join them into a comma-separated string
    column_definitions = [f"{col_info[0]} {col_info[1]}" for col_info in map_column_info]
    # Get the name of the first column for the ORDER BY clause
    order_by_column = map_column_info[0][0]

    # Generate the CREATE TABLE SQL statement with ORDER BY clause
    create_table_sql = f"CREATE TABLE {target_db}.{target_table} on cluster default ({', '.join(column_definitions)}) ENGINE = ReplicatedMergeTree ORDER BY {order_by_column}"

    connection = get_connection("clickhouse", target_db)

    try:
        # Check if the table exists

        orig_columns = get_columns("clickhouse", target_db, target_table)

        logger.info(f"Table {target_db}.{target_table} already exists.")

        # Drop the existing table if it exists and column information matches
        if orig_columns == map_column_info:
            logger.info(
                f"Table {target_db}.{target_table} already exists with the same columns and types. Skipping table creation.")
        else:
            logger.info(
                f"Table {target_db}.{target_table} already exists but have different columns and types,so drop table {target_db}.{target_table}...")
            connection.execute(f"DROP TABLE {target_db}.{target_table}")
            logger.info("Waiting for 10 minutes because clickhouse drop table need time to delete the metadata ...")
            time.sleep(600)
            logger.info(f"Executing SQL to create table {target_db}.{target_table}:")
            connection.execute(create_table_sql)
            logger.info(f"Table {target_db}.{target_table} created successfully.")
    except Exception as e:
        # If the table doesn't exist, log the message and continue
        if "Table" in str(e) and "doesn't exist" in str(e):
            logger.info(f"Table {target_db}.{target_table} does not exist. Proceeding with table creation...")
            # Execute the CREATE TABLE SQL statement
            logger.info(f"Executing SQL to create table {target_db}.{target_table}:")
            logger.info(f"Table {target_db}.{target_table} created by:{create_table_sql}")
            connection.execute(create_table_sql)
            logger.info(f"Table {target_db}.{target_table} created successfully.")
        else:
            logger.error(f"Failed to create table {target_db}.{target_table}: {str(e)}")
            raise e
    finally:
        connection.disconnect()


def create_table_maxcompute(target_db, target_table, map_column_info):
    connection = ODPS(odps_access_id, odps_access_key, odps_project, endpoint=odps_endpoint)
    odps_columns = [f"{col_info[0]} {col_info[1]}" for col_info in map_column_info]

    # Check if the last column is already "mc_create_at"
    last_column_name, last_column_type = map_column_info[-1]
    if last_column_name.lower() != "mc_create_at":
        # Add the extra field "mc_create_at" at the end of the column definitions
        odps_columns.append("mc_create_at string")

    # Generate the CREATE TABLE SQL statement
    create_table_sql = "CREATE TABLE {}.{} (\n    {}\n)".format(target_db, target_table, ',\n    '.join(odps_columns))

    # Check if the table already exists
    try:

        # If the table exists, drop it first
        connection.execute_sql(f"DROP TABLE {target_db}.{target_table}")
        logger.info(f"Table {target_db}.{target_table} already exists. Dropping the existing table...")
    except errors.NoSuchObject:
        # If the table does not exist, proceed to create it
        pass

    # Execute the SQL statement to create the table in MaxCompute
    logger.info(f"Executing SQL to create table {target_db}.{target_table}:")
    logger.info(f"Table {target_db}.{target_table} created by:{create_table_sql}")
    connection.execute_sql(create_table_sql)
    logger.info(f"Table {target_db}.{target_table} created successfully.")


def generateSql_and_create_table(map_column_info, target_db_type, target_db, target_table):
    if target_db_type == "mysql":
        create_table_mysql(target_db, target_table, map_column_info)
    elif target_db_type == "clickhouse":
        create_table_clickhouse(target_db, target_table, map_column_info)
    elif target_db_type == "maxcompute":
        create_table_maxcompute(target_db, target_table, map_column_info)
    else:
        raise ValueError("Unsupported target database type.")


def gen_datax_json_config(sourcedbtype, sourcedb, sourcetable, targetdbtype, targetdb, targettable, filename):
    output_path = "/opt/module/datax/job/import"
    # Populate reader and writer configurations based on the database types
    source_column_info = get_columns(sourcedbtype, sourcedb, sourcetable)
    source_column_names = [col[0] for col in source_column_info]
    target_column_info = get_columns(targetdbtype, targetdb, targettable)
    target_column_names = [col[0] for col in target_column_info]

    if sourcedbtype == "mysql" and targetdbtype == "maxcompute":
        # Add mc_create_at column to mysql_column_names if it's missing and exists in odps_column_names
        if target_column_names[-1].lower() == "mc_create_at" and target_column_names[-1].lower() != "mc_create_at":
            source_column_names.append("now()")

        job = {
            "job": {
                "setting": {
                    "speed": {"channel": 8},
                    "errorLimit": {"record": 0, "percentage": 0.02}
                },
                "content": [{
                    "reader": {
                        "name": "mysqlreader",
                        "parameter": {
                            "username": mysql_user,
                            "password": mysql_passwd,
                            "column": source_column_names,
                            "splitPk": "",
                            "connection": [{
                                "table": [sourcetable],
                                "jdbcUrl": [
                                    f"jdbc:mysql://{mysql_host}:{mysql_port}/{sourcedb}"]
                            }]
                        }
                    },
                    "writer": {
                        "name": "odpswriter",
                        "parameter": {
                            "project": odps_project,
                            "table": targettable,
                            "partition": "",
                            "column": target_column_names,
                            "accessId": odps_access_id,
                            "accessKey": odps_access_key,
                            "truncate": True,
                            "odpsServer": odps_endpoint
                        }
                    }
                }]
            }
        }
    elif sourcedbtype == "maxcompute" and targetdbtype == "mysql":
        job = {
            "job": {
                "setting": {
                    "speed": {
                        "channel": 8
                    },
                    "errorLimit": {
                        "record": 0,
                        "percentage": 0.02
                    }
                },
                "content": [{
                    "reader": {
                        "name": "odpsreader",
                        "parameter": {
                            "accessId": odps_access_id,
                            "accessKey": odps_access_key,
                            "project": odps_project,
                            "table": sourcetable,
                            "column": source_column_names,
                            "odpsServer": odps_endpoint
                        }
                    },
                    "writer": {
                        "name": "mysqlwriter",
                        "parameter": {
                            "writeMode": "replace",
                            "username": mysql_user,
                            "password": mysql_passwd,
                            "column": target_column_names,
                            "connection": [{
                                "jdbcUrl": f"jdbc:mysql://{mysql_host}:{mysql_port}/{targetdb}?useSSL=false&verifyServerCertificate=false",
                                "table": [targettable]

                            }]
                        }
                    }
                }]
            }
        }
    elif sourcedbtype == "maxcompute" and targetdbtype == "clickhouse":
        job = {
            "job": {
                "content": [
                    {
                        "reader": {
                            "name": "odpsreader",
                            "parameter": {
                                "accessId": odps_access_id,
                                "accessKey": odps_access_key,
                                "project": odps_project,
                                "table": sourcetable,
                                "column": source_column_names,
                                "odpsServer": odps_endpoint
                            }
                        },
                        "writer": {
                            "name": "clickhousewriter",
                            "parameter": {
                                "batchByteSize": 134217728,
                                "batchSize": 65536,
                                "column": target_column_names,
                                "connection": [
                                    {
                                        "jdbcUrl": f"jdbc:clickhouse://{clickhouse_host}:8123/{targetdb}",
                                        "table": [targettable]
                                    }
                                ],
                                "password": clickhouse_passwd,
                                "username": clickhouse_user,
                                "writeMode": "insert"
                            }
                        }
                    }
                ],
                "setting": {
                    "speed": {
                        "channel": "8"
                    }
                }
            }
        }
    else:
        raise ValueError("Unsupported target database type: {}".format(targetdbtype))
        # Generate JSON string from the datax_config dictionary
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    with open(filename, "w") as f:
        json.dump(job, f, indent=4)
    logger.info(job)


def generate_filename(sourcedbtype, sourcedb, sourcetable, targetdbtype, targetdb, targettable):
    target_directory = "/opt/module/datax/job/import"

    if sourcedbtype == "maxcompute" and targetdbtype == "maxcompute":
        filename = f"{target_directory}/{sourcedbtype}_{sourcetable}_2_{targetdbtype}_{targettable}.json"
    elif sourcedbtype == "maxcompute":
        filename = f"{target_directory}/{sourcedbtype}_{sourcetable}_2_{targetdbtype}_{targetdb}.{targettable}.json"
    elif targetdbtype == "maxcompute":
        filename = f"{target_directory}/{sourcedbtype}_{sourcedb}.{sourcetable}_2_{targetdbtype}_{targettable}.json"
    else:
        filename = f"{target_directory}/{sourcedbtype}_{sourcedb}.{sourcetable}_2_{targetdbtype}_{targetdb}.{targettable}.json"

    return filename


def execute_datax(filename):
    # Execute the DataX job using the generated config file
    command = f"python3.7 /opt/module/datax/bin/datax.py {filename}"
    os.system(command)


def main(args):
    try:
        logger.info(
            f"Getting column and data type information from the source table {args.sourcedb}.{args.sourcetable}...")
        source_column_info = get_columns(args.sourcedbtype, args.sourcedb, args.sourcetable)

        logger.info(
            f"Mapping columns between source ({args.sourcedbtype}) and target ({args.targetdbtype}) databases...")
        mapped_column_info = map_columns(source_column_info, args.sourcedbtype, args.targetdbtype)

        logger.info(f"Creating the target table {args.targetdb}.{args.targettable}...")
        generateSql_and_create_table(mapped_column_info, args.targetdbtype, args.targetdb, args.targettable)
        logger.info("Table creation process completed successfully.")

        logger.info("Generating DataX JSON configuration file...")
        filename = generate_filename(args.sourcedbtype, args.sourcedb, args.sourcetable,
                                     args.targetdbtype, args.targetdb, args.targettable)
        gen_datax_json_config(args.sourcedbtype, args.sourcedb, args.sourcetable,
                              args.targetdbtype, args.targetdb, args.targettable, filename)

        logger.info("Performing data transfer using DataX...")
        execute_datax(filename)
        logger.info("Data transfer completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Replicate database table structure and create corresponding tables in the target database")
    parser.add_argument('-stype', '--sourcedbtype', required=True, help="Source database type")
    parser.add_argument('-sdb', '--sourcedb', required=True, help="Source database name")
    parser.add_argument('-st', '--sourcetable', required=True, help="Source table name")
    parser.add_argument('-ttype', '--targetdbtype', required=True, help="Target database type")
    parser.add_argument('-tdb', '--targetdb', required=True, help="Target database name")
    parser.add_argument('-tt', '--targettable', required=True, help="Target table name")
    args = parser.parse_args()

    main(args)
