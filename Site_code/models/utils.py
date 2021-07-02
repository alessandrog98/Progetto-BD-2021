
def denyUpdate(connection, table_name):
    trigger_name = "deny_update" + table_name

    connection.execute("""
        CREATE OR REPLACE FUNCTION deny_update() 
        RETURNS TRIGGER as $$
        BEGIN
           RETURN NULL;
        END;
        $$ LANGUAGE plpgsql""")

    connection.execute("""
                DROP TRIGGER IF EXISTS """ + trigger_name + """ ON """ + table_name + """;
                CREATE TRIGGER """ + trigger_name + """
                AFTER INSERT ON """ + table_name + """
                FOR EACH ROW
                EXECUTE PROCEDURE deny_update()""")
