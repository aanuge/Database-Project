import datetime

from src.swen344_db_utils import connect


def rebuildTables():
    """
    Create the tables. If they already exist, drop them then create them again.
    :return: null
    """
    conn = connect()
    cur = conn.cursor()
    drop_users = """
        DROP TABLE IF EXISTS users
    """
    drop_messages = """
        DROP TABLE IF EXISTS messages
    """
    drop_csv_messages = """
        DROP TABLE IF EXISTS csv_messages
    """
    drop_arrakis_members = """
        DROP TABLE IF EXISTS arrakis_members
    """
    drop_comedy_members = """
            DROP TABLE IF EXISTS comedy_members
        """
    drop_arrakis_channels = """
            DROP TABLE IF EXISTS arrakis_channels
        """
    drop_comedy_channels = """
            DROP TABLE IF EXISTS comedy_channels
        """
    drop_arrakis_messages = """
            DROP TABLE IF EXISTS arrakis_messages
        """
    drop_comedy_messages = """
            DROP TABLE IF EXISTS comedy_messages
        """
    create_users = """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(30) NOT NULL UNIQUE,
            unread_count INTEGER NOT NULL DEFAULT 0,
            email VARCHAR(40) NOT NULL DEFAULT 'user@email.com',
            phone VARCHAR(12) NOT NULL DEFAULT '012-345-6789',
            usernamechange TIMESTAMP NOT NULL DEFAULT '0001-01-01'
        )
    """  # will remove suspension from this table
    create_messages = """
        CREATE TABLE messages (
            id SERIAL PRIMARY KEY,
            sender VARCHAR(30) NOT NULL,
            recipient VARCHAR(30) NOT NULL,
            content VARCHAR(300) NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            status VARCHAR(6) NOT NULL DEFAULT 'unread'
        )
    """  # represents direct messages
    create_csv_messages = """
        CREATE TABLE csv_messages (
            id SERIAL PRIMARY KEY,
            sender VARCHAR(30) NOT NULL,
            recipient VARCHAR(30) NOT NULL,
            content VARCHAR(300) NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            status VARCHAR(6) NOT NULL DEFAULT 'unread'
        )
    """
    create_arrakis_members = """
            CREATE TABLE arrakis_members (
                id SERIAL PRIMARY KEY,
                username VARCHAR(30) NOT NULL,
                user_id INTEGER NOT NULL,
                suspension TIMESTAMP NOT NULL DEFAULT '0001-01-01'
                )
        """
    create_comedy_members = """
                CREATE TABLE comedy_members (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(30) NOT NULL,
                    user_id INTEGER NOT NULL,
                    suspension TIMESTAMP NOT NULL DEFAULT '0001-01-01'
                    )
        """
    create_arrakis_channels = """
                    CREATE TABLE arrakis_channels (
                        id SERIAL PRIMARY KEY,
                        channel_name VARCHAR(30) NOT NULL
                        )
        """
    create_comedy_channels = """
                    CREATE TABLE comedy_channels (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(30) NOT NULL
                        )
        """
    create_comedy_messages = """
                        CREATE TABLE comedy_messages (
                            id SERIAL PRIMARY KEY,
                            channel_id INTEGER NOT NULL,
                            sender VARCHAR(30) NOT NULL,
                            content VARCHAR(300),
                            timestamp TIMESTAMP NOT NULL
                            )
        """
    create_arrakis_messages = """
                        CREATE TABLE arrakis_messages (
                            id SERIAL PRIMARY KEY,
                            channel_id INTEGER NOT NULL,
                            sender VARCHAR(30) NOT NULL,
                            content VARCHAR(300),
                            timestamp TIMESTAMP NOT NULL
                            )
            """
    cur.execute(drop_users)
    cur.execute(drop_messages)
    cur.execute(drop_csv_messages)
    cur.execute(drop_arrakis_members)
    cur.execute(drop_comedy_members)
    cur.execute(drop_arrakis_channels)
    cur.execute(drop_comedy_channels)
    cur.execute(drop_arrakis_messages)
    cur.execute(drop_comedy_messages)

    cur.execute(create_users)
    cur.execute(create_messages)
    cur.execute(create_csv_messages)

    cur.execute(create_arrakis_members)
    cur.execute(create_comedy_members)
    cur.execute(create_arrakis_channels)
    cur.execute(create_comedy_channels)
    cur.execute(create_arrakis_messages)
    cur.execute(create_comedy_messages)
    conn.commit()
    conn.close()


def insert_data():
    """
    Insert test data into the tables
    :return: null
    """
    conn = connect()
    cur = conn.cursor()
    insert_users = """
            INSERT INTO users(username, unread_count)
                        VALUES('Abbott', DEFAULT),
                        ('Costello', 1),
                        ('Moe', 1),
                        ('Larry', DEFAULT),
                        ('Curly', 1),
                        ('Bob', DEFAULT),
                        ('DrMarvin', 1),
                        ('spicelover', DEFAULT),
                        ('Paul', DEFAULT);
            """
    cur.execute(insert_users)
    insert_messages = """
            INSERT INTO messages(sender, recipient, content, timestamp, status)
                        VALUES ('Larry', 'Costello', 'Larry to Costello 1956', '1956-05-06 00:00:00', DEFAULT),
                        ('Abbott', 'Costello', 'Abbott to Costello 1923', '1923-02-03 00:00:00', 'read'),
                        ('Costello', 'Abbott', 'Costello to Abbott 1940', '1940-04-04 00:00:00', 'read'),
                        ('Curly', 'Abbott', 'Curly to Abbott 1960', '1960-06-06 00:00:00', 'unread'),
                        ('Moe', 'Larry', 'Moe to Larry 1970', '1970-07-07 00:00:00', 'read'),
                        ('Larry', 'Moe', 'Larry to Moe 1955', '1955-05-05 00:00:00', 'read'),
                        ('Paul', 'Moe', 'Paul to Moe 1955', '2055-05-05 00:00:00', 'read'),
                        ('Moe', 'Paul', 'Moe to Paul 1955', '2055-05-05 00:00:00', 'read'),
                        ('Moe', 'Paul', 'dingus', '2055-05-06 00:00:00', 'read');
            """
    cur.execute(insert_messages)
    insert_comedy_members = """
            INSERT INTO comedy_members(username, user_id, suspension)
                        VALUES('Abbott', 1, DEFAULT),
                        ('Costello', 2, DEFAULT),
                        ('Moe', 3, DEFAULT),
                        ('Larry', 4, DEFAULT),
                        ('Curly', 5, DEFAULT),
                        ('Bob', 6, DEFAULT),
                        ('DrMarvin', 7, DEFAULT);
            """
    cur.execute(insert_comedy_members)
    insert_arrakis_members = """
                INSERT INTO arrakis_members(username, user_id, suspension)
                            VALUES('spicelover', 8, DEFAULT);
                """
    cur.execute(insert_arrakis_members)
    insert_comedy_channels = """
                INSERT INTO comedy_channels(name)
                            VALUES('#ArgumentClinic'),
                            ('#Dialog');
                """
    cur.execute(insert_comedy_channels)
    insert_arrakis_channels = """
                INSERT INTO arrakis_channels(channel_name)
                            VALUES('#Worms'),
                            ('#Random');
                """
    cur.execute(insert_arrakis_channels)
    conn.commit()
    conn.close()


def insert_csv_data():
    """
    Function made to insert the csv test data into its table
    :return: null
    """
    conn = connect()
    cur = conn.cursor()
    abbott_sender = """
            INSERT INTO csv_messages(sender, recipient, content, timestamp)
            VALUES ('Abbott', 'Costello', (%s), '2022-02-01');
        """
    costello_sender = """
                INSERT INTO csv_messages(sender, recipient, content, timestamp)
                VALUES ('Costello', 'Abbott', (%s), '2022-02-01');
        """
    csv_file = open('whos_on_first.csv', 'r')
    line_count = 0
    while True:
        line_count += 1
        line = csv_file.readline()

        if not line:
            break

        sep = line.index(', ')  # The delimiter

        if line_count > 1:
            if line[sep + 2] == ' ':
                sep += 1
            if line[0:sep - 1] == 'Abbott':
                cur.execute(abbott_sender, [line[sep + 2:]])
            elif line[0:sep - 1] == 'Costello':
                cur.execute(costello_sender, [line[sep + 2:]])
            else:
                cur.execute(costello_sender, [line[sep + 2:]])
                cur.execute(abbott_sender, [line[sep + 2:]])

    csv_file.close()
    conn.commit()
    conn.close()


def get_messages_between_users(person1, person2):
    """
    Retrieves all messages sent between two specified user
    :param person1: First user
    :param person2: Second user
    :return: List of tuples containing the messages
    """
    conn = connect()
    cur = conn.cursor()
    getmessages = f"""
                    SELECT content 
                    FROM messages 
                    WHERE sender = (%s) 
                    AND recipient = (%s)
                    OR sender = (%s)
                    AND recipient = (%s)
        """
    cur.execute(getmessages, [person1, person2, person2, person1])
    messages_to_return = cur.fetchall()
    conn.close()
    return messages_to_return


def get_messages_during_year(person1, person2, year):
    """
    Retrieves all messages between two specified users during a specified year
    :param person1: First user
    :param person2: Second user
    :param year: Desired year to retrieve messages from
    :return: List of tuples containing the messages
    """
    conn = connect()
    cur = conn.cursor()
    getmessages = f"""
                            SELECT content 
                            FROM messages 
                            WHERE sender = (%s)
                            AND recipient = (%s)
                            AND timestamp = (%s)
                            OR sender = (%s)
                            AND recipient = (%s)
                            AND timestamp = (%s) 
                """
    cur.execute(getmessages, [person1, person2, year, person2, person1, year])
    messages_to_return = cur.fetchall()
    conn.close()
    return messages_to_return


def get_unread_direct_messages(user):
    """
    Retrieves all unread direct messages sent to a particular user
    :param user: The user to retrieve unread messages for
    :return: List of tuples containing the unread messages
    """
    conn = connect()
    cur = conn.cursor()
    select_unread = f"""
                            SELECT content 
                            FROM messages 
                            WHERE recipient = (%s)
                            AND status = 'unread'
                    """
    cur.execute(select_unread, [user])
    count = len(cur.fetchall())
    conn.close()
    return count


def is_member(user, community):
    """
    check if the user is part of the community
    :param user: user being checked
    :param community: community being checked
    :return: True if they are, False if they are not
    """
    conn = connect()
    cur = conn.cursor()
    check_if_member = """
            SELECT username
            FROM {}_members
            WHERE username = '{}'
    """
    cur.execute(check_if_member.format(community, user))
    result = cur.fetchall()
    if len(result) == 0:
        print(user, ' is not a member of ', community)
        return False
    else:
        return True

def is_suspended(person, current_date, community):
    """
    Check if a certain user is suspended at a date for a community
    :param person: Person to check suspension for
    :param current_date: The date to check for suspension on
    :param community: The community to check suspension for
    :return: True if the user is suspended, False if they are not
    """
    conn = connect()
    cur = conn.cursor()
    if is_member(person, community) is False:
        return False
    check_suspension = """
                                SELECT suspension
                                FROM {}_members
                                WHERE username = \'{}\'
                        """
    cur.execute(check_suspension.format(community, person))
    result = cur.fetchall()
    conn.close()
    r1 = result[0][0]
    r2 = datetime.datetime(int(current_date[0:4]), int(current_date[5:7]), int(current_date[8:10]))
    # return True if they are still suspended, False if they are not
    if r1 > r2:
        print(person, 'is still suspended until', r1)
        return True
    print(person, 'is not suspended')
    return False


def get_messages_between_dates(date1, date2):
    """
    Retrieves all messages sent by all users between two
    :param date1: Lower limit date
    :param date2: Upper limit date
    :return: List of tuples containing messages between the dates
    """
    conn = connect()
    cur = conn.cursor()
    getmessages = f"""
                                SELECT content 
                                FROM messages 
                                WHERE timestamp > (%s)
                                AND timestamp < (%s)
                    """
    cur.execute(getmessages, [date1, date2])
    messages_to_return = cur.fetchall()
    conn.close()
    return messages_to_return


def count_users():
    """
    Counts how many users are registered in the system
    :return: Integer representing the number of users
    """
    conn = connect()
    cur = conn.cursor()
    countusers = """
                                SELECT id 
                                FROM users 
                    """
    count = 0
    cur.execute(countusers)
    for x in cur.fetchall():
        count += 1
    return count


def count_messages():
    """
    Counts total messages that have been sent by all users
    :return: Integer representing total number of messages
    """
    conn = connect()
    cur = conn.cursor()
    countmessages = """
                                SELECT content 
                                FROM messages 
                    """
    count = 0
    cur.execute(countmessages)
    for x in cur.fetchall():
        count += 1
    return count


def count_csv_messages():
    """
    Counts total messages that were in the csv file
    :return: Integer representing total number of messages in the csv file
    """
    conn = connect()
    cur = conn.cursor()
    countmessages = """
                                SELECT content 
                                FROM csv_messages 
                    """
    count = 0
    cur.execute(countmessages)
    for x in cur.fetchall():
        count += 1
    return count


def get_csv_messages():
    """
    Get all the messages in csv_messages
    :return: List of tuples of the messages
    """
    conn = connect()
    cur = conn.cursor()
    getcsvmessages = f"""
                                    SELECT content
                                    FROM csv_messages
                            """
    cur.execute(getcsvmessages)
    messages = cur.fetchall()
    conn.close()
    return messages


def read_messages_sent_by_user(person):
    """
    Counts how many messages have been sent by a user that have been read
    :param person: User to check sent messages for
    :return: The number of read messages the user has sent
    """
    conn = connect()
    cur = conn.cursor()
    getmessages = f"""
                        SELECT content 
                        FROM messages 
                        WHERE sender = (%s)
                        AND status = 'read'
            """
    cur.execute(getmessages, [person])
    count = 0
    for x in cur.fetchall():
        count += 1
    return count


def send_direct_message(sender, recipient, current_date, content):
    """
    Send a message
    :param sender: The sender of the message
    :param recipient: The recipient of the message
    :param current_date: The timestamp of the message
    :param content: The content of the message being sent
    :return: null
    """
    conn = connect()
    cur = conn.cursor()
    sendmessage = f"""
                        INSERT INTO messages(sender, recipient, timestamp, content)
                        VALUES((%s), (%s), (%s), (%s))
            """
    cur.execute(sendmessage, [sender, recipient, current_date, content])
    print('Direct message sent')
    increase_unread_by_1(recipient)
    conn.commit()
    conn.close()


def send_channel_message(community, channel, user, message, current_date):
    """
    Send a message to a channel
    :param community: The community
    :param channel: The channel to send to
    :param user: The sender
    :param message: What the message says
    :param current_date: The timestamp
    :return: null
    """
    conn = connect()
    cur = conn.cursor()
    if is_suspended(user, current_date, community) is False:
        sendmessage = """
                INSERT INTO {}_messages(channel_id, sender, content, timestamp)
                VALUES({}, \'{}\', \'{}\', \'{}\')
        """
        cur.execute(sendmessage.format(community, channel, user, message, current_date))
        print(user, ' sent a message')
        get_users_to_update = """
                SELECT username
                FROM {}_members
                WHERE username != \'{}\'
        """
        cur.execute(get_users_to_update.format(community, user))
        for x in cur.fetchall():
            increase_unread_by_1(x[0])
    conn.commit()
    conn.close()


def messages_sent_by_user(sender):
    """
    Counts how many total messages a user has sent
    :param sender: User to count sent messages for
    :return: Integer: Total number of messages the user has sent
    """
    conn = connect()
    cur = conn.cursor()
    getmessages = f"""
                            SELECT content 
                            FROM messages 
                            WHERE sender = (%s)
                """
    cur.execute(getmessages, [sender])
    count = 0
    for x in cur.fetchall():
        count += 1
    return count


def get_users_who_sent_messages(recipient):
    """
    Retrieves and prints all users that have sent a message to a specified user
    :param recipient: The user we are checking senders for. This will include any user who has sent a message to them
    :return: null
    """
    conn = connect()
    cur = conn.cursor()
    getmessages = f"""
                                SELECT sender 
                                FROM messages 
                                WHERE recipient = (%s)
                    """
    cur.execute(getmessages, [recipient])
    result = cur.fetchall()
    for x in result:
        print(x[0])
    conn.close()


def read_direct_message(id):
    """
    Change a message status to read
    :param id: The id of the message that will be read
    :return: null
    """
    conn = connect()
    cur = conn.cursor()
    markasread = f"""
                                    UPDATE messages  
                                    SET status = 'read'
                                    WHERE id = (%s)
                        """
    cur.execute(markasread, [id])
    get_recipient = """
            SELECT recipient
            FROM messages
            WHERE id = (%s)
    """
    cur.execute(get_recipient, [id])
    username = cur.fetchall()[0][0]
    decrease_unread_by_1(username)
    conn.commit()
    conn.close()


def get_user_unread_count(user):
    """
    get the unread count of the user
    :param user: the user
    :return: the user's unread count
    """
    conn = connect()
    cur = conn.cursor()
    get_unread = """
            SELECT unread_count
            FROM users
            WHERE username = (%s)
    """
    cur.execute(get_unread, [user])
    count = cur.fetchall()[0][0]
    conn.close()
    return count


def increase_unread_by_1(user):
    """
    increment unread count of user by 1
    :param user: the user
    :return: null
    """
    conn = connect()
    cur = conn.cursor()
    new_value = get_user_unread_count(user) + 1
    update = f"""
                                UPDATE users  
                                SET unread_count = (%s)
                                WHERE username = (%s)
                        """
    cur.execute(update, [new_value, user])
    conn.commit()
    conn.close()


def decrease_unread_by_1(user):
    """
    deincrement a user's unread count by 1
    :param user: the user
    :return: null
    """
    conn = connect()
    cur = conn.cursor()
    new_value = get_user_unread_count(user) - 1
    update = f"""
                                    UPDATE users  
                                    SET unread_count = (%s)
                                    WHERE username = (%s)
                            """
    cur.execute(update, [new_value, user])
    conn.commit()
    conn.close()


def change_name(oldusername, newusername, current_date):
    """
    Change the name of a user in the system and impose a 6 month restriction on when they can do it again
    :param oldusername: The username of the user trying to change their username
    :param newusername: The username the user wishes to switch to
    :param current_date: The date of the username switch
    :return: null
    """
    conn = connect()
    cur = conn.cursor()
    olddate = datetime.datetime(int(current_date[0:4]), int(current_date[5:7]), int(current_date[8:10]))

    newday = olddate.day
    newmonth = (olddate.month + 6) % 12
    newyear = olddate.year + ((olddate.month + 6) // 12)
    newdate = datetime.datetime(newyear, newmonth, newday)
    changeusername = f"""
                                UPDATE users 
                                SET username = (%s), usernamechange = (%s)
                                WHERE username = (%s)
                                AND usernamechange < (%s)
                    """
    checkifchanged = f"""
                                SELECT username 
                                FROM users
                                WHERE username = (%s)
                    """
    updatesender = f"""
                                UPDATE messages 
                                SET sender = (%s)
                                WHERE sender = (%s)
                    """
    updaterecipient = f"""
                                UPDATE messages
                                SET recipient = (%s)
                                WHERE recipient = (%s)
                    """
    updatecomedy = f"""
                                UPDATE comedy_members 
                                SET username = (%s)
                                WHERE username = (%s)
                    """
    updatearrakis = f"""
                                    UPDATE arrakis_members 
                                    SET username = (%s)
                                    WHERE username = (%s)
                        """
    cur.execute(changeusername, [newusername, newdate, oldusername, current_date])
    cur.execute(checkifchanged, [newusername])
    canchange = len(cur.fetchall())
    if canchange > 0:
        cur.execute(updatesender, [newusername, oldusername])
        cur.execute(updaterecipient, [newusername, oldusername])
        if is_member(oldusername, 'comedy'):
            cur.execute(updatecomedy, [newusername, oldusername])
        if is_member(oldusername, 'arrakis'):
            cur.execute(updatearrakis, [newusername, oldusername])
    conn.commit()
    conn.close()


def get_read_direct_messages(person):
    """
    Retrieve all the messages a user has read
    :param person: The person to gather the read messages for
    :return: List of tuples of the messages the user has read
    """
    conn = connect()
    cur = conn.cursor()
    select_read = f"""
                            SELECT content 
                            FROM messages 
                            WHERE recipient = (%s) 
                            AND status = 'read'
                    """
    cur.execute(select_read, [person])
    messages_to_return = cur.fetchall()
    conn.close()
    return messages_to_return


def select_user(id):
    """
    Retrieves the username associated with the specified user id
    :param id: the user id
    :return: Username associated with the id
    """
    conn = connect()
    cur = conn.cursor()
    select_users = f"""
                                SELECT username 
                                FROM users 
                                WHERE id = (%s)
                        """
    cur.execute(select_users, [id])
    users_to_return = cur.fetchall()
    conn.close()
    return users_to_return


def suspend(user, community):
    """
    Suspend a user from a community
    :param user: User to suspend
    :param community: community they are suspended from
    :param date: Date they are suspended until
    :return:
    """
    conn = connect()
    cur = conn.cursor()
    suspenduser = """
                                    UPDATE {}_members 
                                    SET suspension = '9999-01-01' 
                                    WHERE username = \'{}\'
                        """
    cur.execute(suspenduser.format(community, user))
    print(user, 'has been suspended')
    conn.commit()
    conn.close()


def unsuspend(user, community):
    """
    Unsuspend a user from a community
    :param person: user to be unsuspended
    :param community: Community to be unsuspended from
    :return: null
    """
    conn = connect()
    cur = conn.cursor()
    unsuspenduser = """
                                UPDATE {}_members 
                                SET suspension = '0001-01-01' 
                                WHERE username = \'{}\'
                    """
    cur.execute(unsuspenduser.format(community, user))
    print(user, 'has been unsuspended')
    conn.commit()
    conn.close()


def count_comedy_members():
    """
    Count number of members in comedy
    :return: number of members in comedy
    """
    conn = connect()
    cur = conn.cursor()
    select_users = f"""
                                    SELECT id 
                                    FROM comedy_members 
                            """
    cur.execute(select_users, [id])
    count = 0
    for x in cur.fetchall():
        count += 1
    conn.close()
    return count


def count_arrakis_members():
    """
        Count number of members in arrakis
        :return: number of members in arrakis
        """
    conn = connect()
    cur = conn.cursor()
    select_users = f"""
                                    SELECT id 
                                    FROM arrakis_members 
                            """
    cur.execute(select_users, [id])
    count = 0
    for x in cur.fetchall():
        count += 1
    conn.close()
    return count


def join_community(user_id, username, community_name):
    """
    Join a community
    :param user_id: id of user
    :param username: name of user
    :param community_name: community they are joining
    :return: null
    """
    conn = connect()
    cur = conn.cursor()
    join = """
        INSERT INTO {}_members (user_id, username)
        VALUES({}, \'{}\')
    """
    cur.execute(join.format(community_name, user_id, username))
    conn.commit()
    conn.close()


def leave_community(user_id, community_name):
    """
    leave a community
    :param user_id: id of user
    :param community_name: community they are leaving
    :return:
    """
    conn = connect()
    cur = conn.cursor()
    leave = """
            DELETE FROM {}_members WHERE user_id = {}
        """
    cur.execute(leave.format(community_name, user_id))
    conn.commit()
    conn.close()


def count_mentions(user):
    """
    Gets number of times a user was mentioned
    :param user: User that it being counted for
    :return: Number of times they were @'d
    """
    conn = connect()
    cur = conn.cursor()
    mention = '@' + user
    count = 0
    check_comedy = """
            SELECT content
            FROM comedy_messages
    """
    check_arrakis = """
            SELECT content
            FROM arrakis_messages
    """
    if is_member(user, 'comedy') is True:
        cur.execute(check_comedy)
        results = cur.fetchall()
        for x in results:
            if x[0].find(mention) != -1:
                count += 1

    if is_member(user, 'arrakis') is True:
        cur.execute(check_arrakis)
        results = cur.fetchall()
        for x in results:
            if x[0].find(mention) != -1:
                count += 1
    return count


def search_keyword(community, key):
    """
    Searches a community for messages containing specified text
    :param community: The community to search in
    :param key: the text to search for
    :return: List of tuples with messages containing the key
    """
    conn = connect()
    cur = conn.cursor()
    new_key = key.replace(' ', ' & ')
    search = """
        SELECT content
        FROM {}_messages
        WHERE to_tsvector(content) @@ to_tsquery('{}')
    """
    cur.execute(search.format(community, new_key))
    messages = cur.fetchall()
    conn.close()
    return messages


def moderator_query(community, date1, date2, current_date):
    """
    List all users who have sent a message in a given date range who are currently suspended from any community
    :param community: The specified community
    :param date1: lower date limit
    :param date2: upper date limit
    :param current_date: current date
    :return: List of users who are currently suspended from a community that sent a message in the given time range
    """
    conn = connect()
    cur = conn.cursor()
    getcomedysenders = f"""
                                SELECT sender 
                                FROM comedy_messages 
                                WHERE timestamp > (%s)
                                AND timestamp < (%s)
                    """
    getarrakissenders = f"""
                                SELECT sender 
                                FROM arrakis_messages 
                                WHERE timestamp > (%s)
                                AND timestamp < (%s)
                    """
    getarrakismembers = f"""
                                SELECT username 
                                FROM arrakis_members
                                WHERE suspension > (%s)
    """
    getcomedymembers = f"""
                                SELECT username 
                                FROM comedy_members
                                WHERE suspension > (%s)
        """
    if community == 'comedy':
        cur.execute(getcomedysenders, [date1, date2])
    else:
        cur.execute(getarrakissenders, [date1, date2])

    senders = cur.fetchall()

    if community == 'comedy':
        cur.execute(getcomedymembers, [current_date])
    else:
        cur.execute(getarrakismembers, [current_date])

    suspended_users = cur.fetchall()

    return_this = []

    for x in senders:
        for y in suspended_users:
            if x[0] == y[0]:
                return_this.append(x[0])

    conn.close()
    return return_this


def activity_summary(date):
    """
    print an activty summary for the past 30 days up to the given date
    :param date: given date
    :return:  Null
    """
    conn = connect()
    cur = conn.cursor()
    olddate = datetime.datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]))


    start_date = olddate - datetime.timedelta(30)

    getcomedymessages = """
                        SELECT content 
                        FROM comedy_messages
                        WHERE timestamp > (%s)
                        AND timestamp < (%s)
    """
    cur.execute(getcomedymessages, [start_date, olddate])
    m = cur.fetchall()
    messages = []
    avg_comedy_messages = 0
    for x in m:
        if len(x[0]) > 5:
            avg_comedy_messages += 1
            messages.append(x[0])

    avg_comedy_messages = avg_comedy_messages / 30


    getcomedysenders = """
                        SELECT sender 
                        FROM comedy_messages
                        WHERE content = (%s)
    """
    senders2 = []
    for i in messages:
        cur.execute(getcomedysenders, [i])
        temp = cur.fetchall()
        if len(temp) > 0:
            if temp[0] not in senders2:  # prevent duplicates
                senders2.append(temp[0])
    active_comedy_members = len(senders2)

    getarrakismessages = """
                            SELECT content 
                            FROM arrakis_messages
                            WHERE timestamp > (%s)
                            AND timestamp < (%s)
        """
    cur.execute(getarrakismessages, [start_date, olddate])
    m = cur.fetchall()
    messages = []
    avg_arrakis_messages = 0
    for x in m:
        if len(x[0]) > 5:
            avg_arrakis_messages += 1
            messages.append(x[0])

    avg_arrakis_messages = avg_arrakis_messages / 30

    getarrakissenders = """
                            SELECT sender 
                            FROM arrakis_messages
                            WHERE content = (%s)
        """
    senders2 = []
    for i in messages:
        cur.execute(getarrakissenders, [i])
        temp = cur.fetchall()
        if len(temp) > 0:
            if temp[0] not in senders2:  # prevent duplicates
                senders2.append(temp[0])
    active_arrakis_members = len(senders2)

    print_statement = [
        {'community': 'Arrakis', 'avg_arrakis_messages': avg_arrakis_messages, 'active_arrakis_members': active_arrakis_members},
        {'community': 'Comedy', 'avg_comedy_messages': avg_comedy_messages, 'active_comedy_members': active_comedy_members}
    ]
    print(print_statement)
    conn.close()
