from sqlalchemy import create_engine
import mysql.connector

def sqls(host,port,user,password,db,dfs,tablename):
    db_connection_str =f'mysql+pymysql://{host}:{password}@{port}/{db}' #접속할 db설정
    db_connection = create_engine(db_connection_str)
    conn = db_connection.connect()
    dfs.to_sql(name=tablename,con=db_connection, if_exists='append',index=False)
    