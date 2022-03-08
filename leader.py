import sqlite3

def sql_connection(db_file):
        con = None
        try:
                con = sqlite3.connect(db_file)
        except sqlite3.Error as e:
                print(e)
        return con

def create_sqlList():
        playerList = []
        playerUnique = []
        player_uptime = 0
        player_final = []
        database = "playtime.db"
        con = sql_connection(database)
        cur = con.cursor()
        cur.execute(" SELECT * FROM playtable;")
        rawList = cur.fetchall()
        con.close()
        # Creating a list of all the players
        for i in rawList:
                playerList.append(i[0])
        #taking duplicate entries out of the list
        playerUnique = list(dict.fromkeys(playerList))
        for i in playerUnique: 
                for player,uptime,time in rawList:
                        if player == i:
                                player_uptime = player_uptime + uptime
#               print(f'{i}s uptime is {player_uptime}')
                player_final.append([i,player_uptime])
                player_uptime = 0
        return player_final


for i in create_sqlList():
        print(f'{i[0]} - {i[1]}')
