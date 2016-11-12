
def ErrorHandler(session):
    try:

        session.rollback()

        #insert to DB
        None
    except:
        # inser to file system on error in DB
        None

# this layer can have definitions to insert alerts, messages etc.