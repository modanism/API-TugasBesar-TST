from sqlalchemy import create_engine
from decouple import config
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values(".env")

# db_user = config["DB_USER"]
db_user = "doadmin"
# db_password = config["DB_PASSWORD"]
db_password = "AVNS_HQ67mah5grQkmlcXlM8"
# db_host = config["DB_HOST"]
db_host = "db-arga-plss-ngerjain-tubes-do-user-10225549-0.b.db.ondigitalocean.com"
# db_port = int(config["DB_PORT"])
db_port = 25060
# db_database = config["DB_DATABASE"]
db_database = "authentication"
# db_sslmode = bool(config["DB_SSLMODE"])
db_engine = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
create_engine(db_engine)
engine = create_engine(db_engine)
conn = engine.connect()