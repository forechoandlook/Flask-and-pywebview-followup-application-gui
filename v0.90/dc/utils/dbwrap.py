import sqlite3
import pandas as pd


class Dbwrap:
    """Basic CRUD database operations using dictionaries"""

    def __init__(self, db_path):
        """Require path to database as parameter"""
        self.db_path = db_path

    def get_connection(self):
        """Connect to a db and if it not exists creates one with the name given"""
        connection = sqlite3.connect(self.db_path)
        return connection


    def execute_query(self, query, keepConn=False):
        """Execute query, commit and close query"""
        try:#execute query in database
            conn = self.get_connection()
            if conn == False:
                raise Exception("Connection to database failed!")
            else:
                with conn:
                    conn.execute(query)
                if keepConn:
                    return True
                else:
                    conn.close()
                    return True
        except Exception as e:#query was not executed, Try again
            raise Exception("Failed to execute query! Got {}".format(str(e)))


    def create_row(self, tableName, infoaddDict):
        """Insert row in db: the dict must contain the column names coresponding to the tableName"""
        processedInfo = {}
        for k, val in infoaddDict.items():
            if isinstance(val, str):
                templi = []
                templi.append(val)
                val = [str(v) for v in templi]
                processedInfo[k] = ','.join(list(set(val)))
            else:
                try:
                    val = [str(v) for v in val]
                    processedInfo[k] = ','.join(list(set(val)))
                except:
                    processedInfo[k] = str(val)

        columns = tuple(processedInfo.keys())
        values = tuple(processedInfo.values())

        sql_insert = """INSERT INTO {} {} VALUES {};"""
        insert = sql_insert.format(tableName, columns, values)

        return self.execute_query(insert)

    
    def read_table(self, table_name, chunk_size=None):
        """Get table from database as a pandas dataframe - sql2df"""
        query = "SELECT * FROM {}".format(table_name)
        conn = self.get_connection()
        df = pd.read_sql_query(query, conn, chunksize=chunk_size)
        conn.close()
        return df
    
    
    def update_row(self, tableName, updatedict, colIDName):
        """Update row in db :The dict must contain the columns which will be updated in the table"""

        colsvals = []
        for col, val in updatedict.items():
            if col != colIDName:
                sqval = col + '=' + "'{}'".format(val)
                colsvals.append(sqval)
            else:
                whereCol_value = col + '=' + "'{}'".format(val)

        colstoUpdate = ', '.join(colsvals)
        sql_update_statement = str("UPDATE " + '{}'.format(tableName) + " SET " + colstoUpdate + " WHERE " + whereCol_value + ";")

        return self.execute_query(sql_update_statement)

    
    def update_cell(self, table_name, coltoUpdate, colValtoUpdate, colID, rowID):
        """Update a table cell with a value"""
        update_batch = """UPDATE "{}" SET "{}"="{}" WHERE "{}"="{}";""".format(table_name, coltoUpdate, colValtoUpdate, colID, rowID)
        return self.execute_query(update_batch)
    
    
    def delete_row(self, table, colID, rowID):
        """Delete row from db"""
        delete_row = """DELETE FROM {} WHERE {}='{}' """.format(table, colID, rowID)
        return self.execute_query(delete_row)


    def prepare_cell(self, cell, tolist=False):
        """Remove whitespaces/new line from the string and put words to list if needed"""
        cell = str(cell).strip().replace('\n', ' ') # using replace to avoid POST\n156424 > POST156424
        cellli = ''.join(cell).split(' ')
        cellli = [c.strip() for c in cellli if len(c) != 0]

        if tolist:
            return cellli
        else:
            cellstr = ' '.join(cellli)
        return cellstr

    def stringify_df(self, df):
        """Clean cells and make all columns astype string"""
        columnsli = df.columns.tolist()
        for col in columnsli:
            df[col] = df[col].apply(lambda cell: self.prepare_cell(cell))
        return df

    def insert_table(self, df, dfname, if_exists="replace"):
        """"Insert table in database if exists replace(default) df2sql"""
        df = self.stringify_df(df)
        conn = self.get_connection()
        df.to_sql(dfname, conn, if_exists=if_exists, index=False)
        conn.commit()
        conn.close()