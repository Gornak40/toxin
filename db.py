from sqlite3 import connect


def makeDB(sizes, links):
    open('.db', 'wb').close()
    con = connect('.db')
    cur = con.cursor()
    com = 'create table main (size real, url string);'
    cur.execute(com)
    for x in zip(sizes, links):
        adding = 'insert into main values (?, ?)'
        cur.execute(adding, x)
    con.commit()


def readDB(val):
    con = connect('.db')
    cur = con.cursor()
    com = 'select url from main where size = {}'.format(val)
    cur.execute(com)
    res = cur.fetchall()[0][0]
    con.close()
    return res