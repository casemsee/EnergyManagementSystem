from configuration.configuration_database import scheduling_plan_local
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def db_session(config = scheduling_plan_local):
    """
    Create database engine for the energy management system
    :return: Database Session
    """
    db_str = 'mysql+pymysql://' + config["user_name"] + ':' + config['password'] + '@' + config['ip_address'] + '/' + config['db_name']
    engine = create_engine(db_str, echo=False)
    Session = sessionmaker(bind=engine)

    return Session