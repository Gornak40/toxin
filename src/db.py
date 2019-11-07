from sqlite3 import connect


def makeDB(name, sizes, links):
    open(name, 'wb').close()
    con = connect(name)
    cur = con.cursor()
    com = 'create table main (size real, url string);'
    cur.execute(com)
    for x in zip(sizes, links):
        adding = 'insert into main values (?, ?)'
        cur.execute(adding, x)
    con.commit()


def readDB(name, val):
    con = connect(name)
    cur = con.cursor()
    com = 'select url from main where size = {}'.format(val)
    cur.execute(com)
    res = cur.fetchall()[0][0]
    con.close()
    return res