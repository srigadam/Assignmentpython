import sqlalchemy as database
import os
from sqlalchemy import create_engine, MetaData,Table, Column, Float,String

def database_insertion(train_df, testing_data, ideal_df, map_data, small_err, data_indices):
    database_file = 'DataBase.database'
    if os.path.isfile(database_file):
       os.remove(database_file)

# Create a new SQLite database
    directory = os.getcwd()
    conn_str = f"sqlite:///{os.path.join(directory, database_file)}"
    engine = create_engine(conn_str, echo=True)
    con = engine.connect()
    metadata = MetaData()

    training_data_table = Table(
    "TrainingData", metadata,
    Column("X", Float),
    Column("Y1", Float),
    Column("Y2", Float),
    Column("Y3", Float),
    Column("Y4", Float)
    )
    training_data_table = Table(
    "IdealData", metadata,
    Column("X", Float),
    Column("Y1", Float),
    Column("Y2", Float),
    Column("Y3", Float),
    Column("Y4", Float)
    )
    training_data_table = Table(
    "MappingData", metadata,
    Column("X", Float),
    Column("Y", Float),
    Column("dY", String),
    Column("IdealFunction", database.String)
    )
    
    metadata.create_all(engine)
    table_train = database.Table("TrainingData", metadata, autoload=True, autoload_with=engine)
    train_query = database.insert(table_train)
    train_data_list = []
    train_row_list = {}

    for i in range(0, train_df.rrows()):
        for u in range(0, train_df.rcols()):
            
            if u == 0:
                train_row_list = {'X': train_df.xy_cell_data(i, u)}
            else:
                train_row_list['Y' + str(u)] = train_df.xy_cell_data(i, u)
        train_data_list.append(train_row_list)
        train_row_list = {}

    con.execute(train_query, train_data_list)
    
    table_ideal = metadata.tables["IdealData"]
    ideal_query = database.insert(table_ideal)

    ideal_list = [
    {
        'X': ideal_df.xy_cell_data(i, 0),
        **{f'Y{u}': ideal_df.xy_cell_data(i, u) for u in range(1, ideal_df.rcols())}
    }
    for i in range(ideal_df.rrows())
    ]

# Run the insert query using the information.
    with engine.connect() as con:
      con.execute(ideal_query, ideal_list)
    
    table_map = metadata.tables["MappingData"]
    map_query = database.insert(table_map)

    map_list = [
    {
        'X': testing_data.xy_cell_data(i, 0),
        'Y': testing_data.xy_cell_data(i, 1),
        'dY': "None" if map_data[i] is None else str(small_err[i]),
        'IdealFunction': "None" if map_data[i] is None else str(data_indices[map_data[i]])
    }
    for i in range(testing_data.rrows())
   ]


    with engine.connect() as con:
       con.execute(map_query, map_list)
   