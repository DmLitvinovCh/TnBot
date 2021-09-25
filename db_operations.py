import sqlite3
import dt_def as dt
import math


connection = None

# функция подключения к бд
def get_connection():
    global connection
    if connection is None:
        connection = sqlite3.connect('nogotok.db', timeout=10, check_same_thread=False)
    return connection

# функция создания таблиц
def init_db(flag : bool = False):
    conn = get_connection()
    curs = conn.cursor()
    try:
        if flag:

            curs.execute('DROP TABLE IF EXISTS users')
            curs.execute('''
                                        CREATE TABLE IF NOT EXISTS users (
                                            id    INTEGER PRIMARY KEY,
                                            name   TEXT NOT NULL,
                                            enabled INTEGER NOT NULL DEFAULT 1,
                                            gcalendarid TEXT 
                                            )'''
                        )
            curs.execute('DROP TABLE IF EXISTS services')
            curs.execute('''
                                                    CREATE TABLE IF NOT EXISTS services (
                                                        id      INTEGER PRIMARY KEY,
                                                        name    TEXT NOT NULL,
                                                        cost    REAL ,
                                                        enabled INTEGER NOT NULL DEFAULT 1
                                                        )'''
                         )
            curs.execute('DROP TABLE IF EXISTS shedule')
            curs.execute('''
                                                    CREATE TABLE IF NOT EXISTS shedule (
                                                        id        INTEGER PRIMARY KEY,
                                                        userid    INTEGER NOT NULL,
                                                        serviceid INTEGER NOT NULL,
                                                        cost REAL,
                                                        creationdate REAL NOT NULL,
                                                        shiftdate INTEGER NOT NULL,
                                                        begintime INTEGER NOT NULL,
                                                        endtime INTEGER NOT NULL,
                                                        enabled INTEGER DEFAULT 1
                                                        )'''
                         )
            curs.execute('DROP TABLE IF EXISTS talons')
            curs.execute('''
                                                    CREATE TABLE IF NOT EXISTS talons (
                                                        id        INTEGER PRIMARY KEY,
                                                        sheduleid    INTEGER NOT NULL,
                                                        creationdate REAL NOT NULL,
                                                        begintime INTEGER NOT NULL,
                                                        endtime   INTEGER NOT NULL,
                                                        booked INTEGER DEFAULT 0,
                                                        enabled INTEGER DEFAULT 1,
                                                        eventid TEXT 
                                                        )'''
                         )
            curs.execute('DROP TABLE IF EXISTS clients')
            curs.execute('''
                                                                CREATE TABLE IF NOT EXISTS clients (
                                                                    id      INTEGER PRIMARY KEY,
                                                                    creationdate REAL NOT NULL,
                                                                    name    TEXT NOT NULL,
                                                                    chatid  INTEGER NOT NULL,
                                                                    telegram_user_id INTEGER,
                                                                    telegram_user_name TEXT,
                                                                    phone   TEXT NOT NULL,
                                                                    enabled INTEGER DEFAULT 1
                                                                    )'''
                         )
            curs.execute('DROP TABLE IF EXISTS booked_talons')
            curs.execute('''
                                                                            CREATE TABLE IF NOT EXISTS booked_talons (
                                                                                talonid  INTEGER NOT NULL,
                                                                                creationdate REAL NOT NULL
                                                                                )'''
                         )
            #curs.execute('SELECT userid, count(userid) FROM shedule WHERE ENABLED = 1 group by userid')
            #print(curs.fetchall())

        conn.commit()
    finally:
        pass #conn.close()


# функция добавления нового сотрудника в бд
def add_worker(name: str):
    conn = get_connection()
    curs = conn.cursor()
    try:
        curs.execute('INSERT INTO users (name) VALUES (?)', (name,))
        conn.commit()
        return 'Запись успешно добавлена! ✅'
    finally:
        pass#conn.close()

# функция получения пользователей
def get_workers(userid):
    conn = get_connection()
    curs = conn.cursor()
    if userid == -1:
        try:
            curs.execute('SELECT id, name FROM users WHERE ENABLED = 1')
            return curs.fetchall()
        finally:
            pass#conn.close()
    else:
        try:
            curs.execute('SELECT id, name FROM users WHERE ENABLED = 1 and id = ?', (userid,))
            return curs.fetchall()
        finally:
            pass#conn.close()

def get_services(servicveid):
    conn = get_connection()
    curs = conn.cursor()
    if servicveid == -1:
        try:
            curs.execute('SELECT id, name, cost FROM services WHERE enabled = 1')
            return curs.fetchall()
        finally:
            pass#conn.close()
    else:
        try:
            curs.execute('SELECT id, name, cost FROM services WHERE enabled = 1 and id = ?', (servicveid,))
            return curs.fetchall()
        finally:
            pass#conn.close()

def get_shedule(userid, shiftdate, sheduleid):
    conn = get_connection()
    curs = conn.cursor()

    if userid == -1 and shiftdate == -1 and sheduleid == -1:
        try:
            curs.execute('''SELECT s.id, u.name ,sr.name, s.shiftdate, s.begintime , s.endtime, s.cost 
                            FROM shedule s 
                            JOIN users u ON u.id = s.userid 
                            JOIN services sr ON sr.id =s.serviceid  
                            WHERE s.enabled = 1 and s.shiftdate >= ?
                            ORDER BY s.shiftdate, s.id 
                            LIMIT 20''', (math.floor(dt.Current_Now())-1,))
            return curs.fetchall()
        finally:
            pass#conn.close()
    elif int(userid) > 0 and int(shiftdate) > 0:
        try:
            curs.execute('''SELECT s.id, u.name ,sr.name, s.shiftdate, s.begintime , s.endtime 
                        FROM shedule s 
                        JOIN users u ON u.id = s.userid 
                        JOIN services sr ON sr.id =s.serviceid  
                        WHERE s.enabled = 1 and s.userid = ? AND s.shiftdate = ?''' , (userid , shiftdate))
            return curs.fetchall()
        finally:
            pass#conn.close()
    elif int(shiftdate) > 0:
        try:
            curs.execute('''SELECT s.id, u.name ,sr.name, s.shiftdate, t.begintime , t.endtime, c.name as client_name, c.phone, s.cost 
                        FROM shedule s 
                        JOIN talons t ON t.sheduleid = s.id
                        JOIN users u ON u.id = s.userid 
                        JOIN services sr ON sr.id = s.serviceid  
                        LEFT JOIN clients c ON c.id = t.booked
                        WHERE s.enabled = 1 AND t.enabled = 1 AND s.shiftdate = ?
                        Order by u.name, s.shiftdate,s.id, s.begintime''', (shiftdate,))
            return curs.fetchall()
        finally:
            pass#conn.close()
    else:
        curs.execute('''SELECT s.id, u.name ,sr.name, s.shiftdate, s.begintime , s.endtime, s.cost 
                                FROM shedule s 
                                JOIN users u ON u.id = s.userid 
                                JOIN services sr ON sr.id =s.serviceid  
                                WHERE s.enabled = 1 and s.id = ?''', (sheduleid, ))
        return curs.fetchall()

def add_user_shedule(shdata, tldata):
    conn = get_connection()
    curs = conn.cursor()

    try:
        curs.executemany('INSERT INTO shedule (userid, serviceid, creationdate, shiftdate, begintime, endtime) VALUES (?,?,?,?,?,?)'
                     , (shdata))

        curs.execute('SELECT last_insert_rowid()')
        sheduleid = curs.fetchone()[0]
        all = []
        for lst in tldata:
            lst.append(sheduleid)
            all.append(lst)

        curs.executemany('INSERT INTO talons( creationdate, begintime, endtime, sheduleid) VALUES (?,?,?,?)'
                         ,  (all))
        curs.execute('''SELECT u.gcalendarid, t.id, s.shiftdate, t.begintime, t.endtime 
                        FROM talons t 
                        JOIN shedule s ON s.id = t.sheduleid 
                        JOIN users u ON u.id = s.userid
                        WHERE t.enabled = 1 and s.id = ?''', (sheduleid,))
        conn.commit()
        return curs.fetchall()
    finally:
        pass  # conn.close()

def get_talons(sheduleid):
    conn = get_connection()
    curs = conn.cursor()

    try:
        curs.execute('''SELECT u.gcalendarid, t.eventid 
                        FROM shedule sh
                        JOIN talons t on sh.id = t.sheduleid
                        JOIN users u on sh.userid = u.id
                        WHERE sh.id = ?''', (sheduleid,))
        return curs.fetchall()
    finally:
        pass#conn.close()


def add_services(name):
    conn = get_connection()
    curs = conn.cursor()
    try:
        #curs.executemany(
            #'INSERT INTO services (name, cost) VALUES (?,?)'
            #, (data,))
        curs.execute('INSERT INTO services (name) VALUES (?)', (name,))
        conn.commit()
        return 'Услуга успешно добавлена ✅'
    finally:
        pass  # conn.close()

def add_booked_talon(talonid):
    conn = get_connection()
    curs = conn.cursor()
    currdt = dt.Current_Now()

    try:
        curs.execute(
            'SELECT talonid FROM booked_talons WHERE talonid = ? and (creationdate + 0.0034722222222222) >= ?'
            , (talonid, currdt))
        bktalonid = curs.fetchone()
        if bktalonid is None:
            curs.execute(
                'INSERT INTO booked_talons (talonid, creationdate) VALUES (?,?)'
                , (talonid, currdt))
            conn.commit()
            return True
        else:
            return False

        conn.commit()
    finally:
        pass  # conn.close()

def del_worker(id):
    conn = get_connection()
    curs = conn.cursor()
    try:
        curs.execute('UPDATE users set enabled = 0 WHERE id = ?', (id,))
        conn.commit()
        return 'Запись успешно удалена'
    finally:
        pass  # conn.close()

def del_service(id):
    conn = get_connection()
    curs = conn.cursor()
    try:
        curs.execute('UPDATE services set enabled = 0 WHERE id = ?', (id,))
        conn.commit()
        return 'Запись успешно удалена'
    finally:
        pass  # conn.close()

def del_shedule(id):
    conn = get_connection()
    curs = conn.cursor()
    try:
        curs.execute('UPDATE shedule set enabled = 0 WHERE id = ?', (id,))
        conn.commit()
        return 'Запись успешно удалена'
    finally:
        pass  # conn.close()

def del_talon(talonid):
    conn = get_connection()
    curs = conn.cursor()
    try:
        curs.execute('UPDATE talons set booked = 0 WHERE id = ?', (talonid,))
        conn.commit()
        return True
    finally:
        pass  # conn.close()

def get_shiftdays_with_free_time(serviceid):
    conn = get_connection()
    curs = conn.cursor()

    try:
        curs.execute('''SELECT distinct s.shiftdate
                        FROM shedule s 
                        JOIN users u ON u.id = s.userid 
                        JOIN services sr ON sr.id =s.serviceid  
                        WHERE s.enabled = 1 and u.enabled = 1 and sr.id = ? and s.shiftdate between ? and ?
                        and exists (select t.id 
                                    from talons t 
                                    where t.sheduleid = s.id 
                                    and t.enabled = 1 
                                    and t.booked = 0
                                    and not exists(select bt.talonid 
                                                    from booked_talons bt 
                                                    where bt.talonid = t.id
                                                    and (bt.creationdate + 0.0034722222222222) >= ? ))
                        ORDER BY s.shiftdate ''', (serviceid, math.floor(dt.Current_Now()) , math.floor(dt.Current_Now()) + 30, dt.Current_Now()))
        return curs.fetchall()
    finally:
        pass  # conn.close()

def get_shedules_days():
    conn = get_connection()
    curs = conn.cursor()

    try:
        curs.execute('''SELECT distinct s.shiftdate 
                        FROM shedule s 
                        JOIN users u ON u.id = s.userid 
                        JOIN services sr ON sr.id =s.serviceid  
                        WHERE s.enabled = 1 and s.shiftdate >= ?
                        ORDER BY s.shiftdate, s.id 
                        LIMIT 30''', (math.floor(dt.Current_Now()) - 1,))
        return curs.fetchall()
    finally:
        pass  # conn.close()

def get_free_shedule_intervals(serviceid, shiftdate):
    conn = get_connection()
    curs = conn.cursor()

    try:
        curs.execute('''SELECT t.id, t.begintime, t.endtime, u.name, s.cost
                        FROM talons t 
                        JOIN shedule s ON s.id = t.sheduleid 
                        JOIN users u ON u.id = s.userid 
                        WHERE t.enabled = 1 and s.enabled = 1 and t.booked = 0 and u.enabled = 1
                        and s.serviceid = ? and s.shiftdate = ?
                        and not exists(select bt.talonid 
                                                    from booked_talons bt 
                                                    where bt.talonid = t.id
                                                    and (bt.creationdate + 0.0034722222222222) >= ? )
                        ORDER BY t.begintime ''', (serviceid, shiftdate, dt.Current_Now()))
        return curs.fetchall()
    finally:
        pass  # conn.close()

def get_talon(talonid):
    conn = get_connection()
    curs = conn.cursor()
    try:
        curs.execute('''SELECT t.id, s.shiftdate,  t.begintime, t.endtime, u.name as username, sr.id as serviceid, sr.name as servicename, s.cost, t.eventid, u.gcalendarid, c.name as client_name, c.phone, c.telegram_user_name 
                        FROM talons t 
                        JOIN shedule s on t.sheduleid = s.id
                        JOIN users u on s.userid = u.id
                        JOIN services sr ON sr.id = s.serviceid
                        LEFT JOIN clients c on c.id = t.booked
                        WHERE t.enabled = 1 and s.enabled = 1
                        and t.id = ?''', (talonid,))
        return curs.fetchone()
    finally:
        pass  # conn.close()

def get_talon_status(talonid):
    conn = get_connection()
    curs = conn.cursor()
    try:
        curs.execute('''SELECT c.id 
                        FROM talons t 
                        JOIN shedule s on t.sheduleid = s.id
                        LEFT JOIN clients c on c.id = t.booked
                        WHERE t.enabled = 1 and s.enabled = 1
            
                        and t.id = ?''', (talonid, ))
        res = curs.fetchone()
        talon_status = res[0]

        if talon_status is None:
            return True
        else:
            return False
    finally:
        pass  # conn.close()

def get_clients_booked_talons(chatid, serviceid):
    conn = get_connection()
    curs = conn.cursor()
    try:
        curs.execute('''SELECT t.id, s.shiftdate,  t.begintime, t.endtime, u.name as username, sr.id as serviceid, sr.name as servicename, s.cost
                        FROM talons t 
                        JOIN shedule s on t.sheduleid = s.id
                        JOIN users u on s.userid = u.id
                        JOIN services sr ON sr.id = s.serviceid
                        JOIN clients c ON c.id = t.booked
                        WHERE t.enabled = 1 and s.enabled = 1
                        and s.shiftdate > ? AND c.chatid = ? and sr.id = ?''', (math.floor(dt.Current_Now()), chatid, serviceid))
        return curs.fetchall()
    finally:
        pass  # conn.close()

def add_booked_talon(talonid):
    conn = get_connection()
    curs = conn.cursor()
    currdt = dt.Current_Now()

    try:
        curs.execute(
            'SELECT talonid FROM booked_talons WHERE talonid = ? and (creationdate + 0.0034722222222222) >= ?'
            , (talonid, currdt))
        bktalonid = curs.fetchone()
        if bktalonid is None:
            curs.execute(
                'INSERT INTO booked_talons (talonid, creationdate) VALUES (?,?)'
                , (talonid, currdt))
            conn.commit()
            return True
        else:
            return False
    finally:
        pass  # conn.close()



def add_client_talon(talonid, chatid, tlg_clientid, client_name, tlg_client_name, phone):

    conn = get_connection()
    curs = conn.cursor()
    currdt = dt.Current_Now()

    try:
        curs.execute(
            'SELECT id FROM talons WHERE id = ? and booked > 0 '
            , (talonid,))
        bktalonid = curs.fetchone()
        if bktalonid is None:
            curs.execute('SELECT id FROM clients WHERE chatid = ? ', (chatid,))
            clid = curs.fetchone()
            if clid is None:
                curs.execute(
                    'INSERT INTO clients (creationdate, name, chatid, telegram_user_id, telegram_user_name, phone) VALUES (?,?,?,?,?,?)'
                    , (currdt, client_name, chatid, tlg_clientid, tlg_client_name, phone))
                curs.execute('SELECT last_insert_rowid()')
                clientid = curs.fetchone()[0]
            else:
                if phone == '':
                    curs.execute(
                        'SELECT phone FROM clients WHERE chatid = ? '
                        , (chatid,))
                    res = curs.fetchone()
                    phone = res[0]

                curs.execute(
                    'UPDATE clients set name = ?, chatid = ?, telegram_user_id = ?, telegram_user_name = ?, phone = ?  WHERE chatid = ?',
                    (client_name, chatid, tlg_clientid, tlg_client_name, str(phone), chatid))
                clientid = clid[0]

            if clientid > 0:
                curs.execute('UPDATE talons set booked = ? WHERE id = ?', (clientid, talonid))
            conn.commit()
            return True
        else:
            return False
    finally:
        pass  # conn.close()


def get_free_talons(serviceid, shiftdate, begintime, chatid):
    conn = get_connection()
    curs = conn.cursor()

    try:
        curs.execute('''SELECT t.id, s.shiftdate,  t.begintime, t.endtime, u.name as username, sr.id as serviceid, sr.name as servicename, s.cost
                        FROM talons t
                        JOIN shedule s on t.sheduleid = s.id
                        JOIN users u on s.userid = u.id
                        JOIN services sr ON sr.id = s.serviceid
                        LEFT JOIN clients c ON c.id = t.booked
                        WHERE t.enabled = 1 and s.enabled = 1 and t.booked = 0 and u.enabled = 1
                        and s.serviceid != ? and s.shiftdate = ? and t.begintime = ?
                        and not exists(select bt.talonid
                                       FROM booked_talons bt
                                        WHERE bt.talonid = t.id
                                        and (bt.creationdate + 0.0034722222222222) >= ? )
                        and not exists (select t2.id 
                                        from talons t2
                                        JOIN shedule s2 on t2.sheduleid = s2.id
                                        JOIN clients c ON c.id = t2.booked
                                        WHERE  s2.serviceid = s.serviceid
                                        and s2.shiftdate > ?
                                        and c.chatid = ?)                    
                        ORDER BY t.begintime ''', (serviceid, shiftdate, begintime, dt.Current_Now(), math.floor(dt.Current_Now()), chatid))
        return curs.fetchall()
    finally:
        pass  # conn.close()

def upd_talon_event(events_info):
    conn = get_connection()
    curs = conn.cursor()
    try:
        curs.executemany('UPDATE talons set eventid = ? WHERE id = ?', events_info)
        conn.commit()
        return True
    finally:
        pass  # conn.close()









