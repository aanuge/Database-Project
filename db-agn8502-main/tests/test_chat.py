import unittest
from src.chat import *
from src.swen344_db_utils import connect


class TestChat(unittest.TestCase):

    # Test building the tables
    def test_a_build_tables(self):
        """Rebuild the tables"""
        conn = connect()
        cur = conn.cursor()
        rebuildTables()
        cur.execute('SELECT * FROM users')
        self.assertEqual([], cur.fetchall(), "no rows in users")
        cur.execute('SELECT * FROM messages')
        self.assertEqual([], cur.fetchall(), "no rows in messages")
        conn.close()

    # Test for idempotency
    def test_b_rebuild_tables_is_idempotent(self):
        """Drop and rebuild the tables twice"""
        rebuildTables()
        rebuildTables()
        conn = connect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users')
        self.assertEqual([], cur.fetchall(), "no rows in users")
        cur.execute('SELECT * FROM messages')
        self.assertEqual([], cur.fetchall(), "no rows in messages")
        conn.close()

    # Test inserting the data into tables
    def test_c_insert_data(self):
        conn = connect()
        insert_data()
        conn.close()

    # Test counting the total users
    def test_d_count_users(self):
        conn = connect()
        print(count_users(), ' users registered')
        self.assertEqual(count_users(), 9)
        conn.close()

    # Test counting total prepopulated messages
    def test_e_count_messages(self):
        conn = connect()
        print(count_messages(), ' total messages sent')
        self.assertEqual(count_messages(), 9)
        conn.close()

    # Test getting messages between 2 users
    def test_f_abbott_costello(self):
        conn = connect()
        result = get_messages_between_users('Abbott', 'Costello')
        totalmessages = 0
        for x in result:
            print(x[0])
            totalmessages += 1
        print(totalmessages, "message(s) between Abbott and Costello")
        self.assertEqual(totalmessages, 2)
        conn.close()

    # Test getting messages between 2 users during a specific year
    def test_g_moe_Larry_1955(self):
        conn = connect()
        result = get_messages_during_year('Larry', 'Moe', '1955-05-05')
        totalmessages = 0
        for x in result:
            print(x[0])
            totalmessages += 1
        print(totalmessages, "message(s) between Moe and Larry during 1995")
        self.assertEqual(totalmessages, 1)
        conn.close()

    # Test getting the number of unread messages a user has
    def test_h_get_unread_direct(self):
        conn = connect()
        result = get_unread_direct_messages('Abbott')
        self.assertEqual(result, 1)
        print('Abbott has ' + str(result) + ' unread message(s)')
        conn.close()

    # Test checking if a user is suspended
    def test_i_check_suspension(self):
        conn = connect()
        self.assertFalse(is_suspended('Larry', '2012-05-04', 'arrakis'))
        self.assertFalse(is_suspended('Curly', '2000-02-29', 'comedy'))
        conn.close()

    # Test getting all messages between 2 dates
    def test_j_messages_between_dates(self):
        conn = connect()
        result = get_messages_between_dates('1923-01-01', '1955-12-31')
        count = 0
        for x in result:
            print(x[0])
            count += 1
        print(count, ' messages between 1923 and 1955')
        self.assertEqual(count, 3)
        conn.close()

    # Test getting the number of messages a user has sent that were read
    def test_k_read_messages_sent_by_user(self):
        conn = connect()
        print('Larry has sent', read_messages_sent_by_user('Larry'), 'read message(s)')
        self.assertEqual(1, read_messages_sent_by_user('Larry'))
        conn.close()

    # Test sending a message
    def test_l_send_direct_message(self):
        conn = connect()
        self.assertEqual(1, messages_sent_by_user('Curly'))
        send_direct_message('Curly', 'Moe', '2000-01-01', 'Curly to Moe 2000')
        print('Curly has sent', messages_sent_by_user('Curly'), 'message(s)')
        self.assertEqual(2, messages_sent_by_user('Curly'))
        conn.close()

    # Test reading a message as well as getting the number of read messages a user has
    def test_m_read_direct_message(self):
        conn = connect()
        result = get_read_direct_messages('Abbott')
        num = 0
        for x in result:
            num += 1
        self.assertEqual(num, 1)
        read_direct_message(4)
        result = get_read_direct_messages('Abbott')
        num = 0
        for x in result:
            num += 1
        self.assertEqual(num, 2)
        print('Abbott has ' + str(num) + ' read message(s)')
        conn.close()

    # Test the flow of sending messages using the send_direct_message method
    def test_n_message_flow(self):
        conn = connect()
        # syntax error when I try to do this with \'
        send_direct_message('Bob', 'DrMarvin', '1991-05-18', 'Im doing the work, Im baby-stepping')
        result = get_messages_between_users('Bob', 'DrMarvin')
        totalmessages = 0
        for x in result:
            totalmessages += 1
        print(totalmessages, "message(s) between Bob and DrMarvin")
        self.assertEqual(totalmessages, 1)

        change_name('Bob', 'BabySteps2Door', '1991-05-19')
        result = get_messages_between_users('BabySteps2Door', 'DrMarvin')
        totalmessages = 0
        for x in result:
            print(x[0])
            totalmessages += 1
        print(totalmessages, "message(s) between BabySteps2Door and DrMarvin")
        self.assertEqual(totalmessages, 1)

        change_name('BabySteps2Door', 'BabySteps2Elevator', '1991-05-20')
        result = get_messages_between_users('BabySteps2Elevator', 'DrMarvin')
        totalmessages = 0
        for x in result:
            print(x[0])
            totalmessages += 1
        print(totalmessages, "message(s) between BabySteps2Elevator and DrMarvin")
        self.assertEqual(totalmessages, 0)

        unread = get_unread_direct_messages('DrMarvin')
        self.assertEqual(unread, 1)
        print('DrMarvin unread messages: ', str(unread))
        get_users_who_sent_messages('DrMarvin')
        conn.close()

    # Test to make sure you can't send a message while suspended
    def test_o_send_while_suspended(self):
        conn = connect()
        suspend('BabySteps2Door', 'comedy')
        send_channel_message('comedy', 1, 'BabySteps2Door', 'DaBaby', '2000-01-01')
        conn.close()

    # Test that the messages from the csv file were added correctly
    def test_p_parse_csv(self):
        insert_csv_data()
        count = count_csv_messages()
        self.assertEqual(187, count)

    def test_q_join_and_leave_community(self):
        self.assertEqual(count_comedy_members(), 7)
        join_community(8, 'spicelover', 'comedy')
        self.assertEqual(count_comedy_members(), 8)
        leave_community(8, 'comedy')
        self.assertEqual(count_comedy_members(), 7)
        self.assertEqual(count_arrakis_members(), 1)
        join_community(9, 'Paul', 'arrakis')
        self.assertEqual(count_arrakis_members(), 2)

    def test_r_send_channel_message(self):
        conn = connect()
        self.assertEqual(0, count_mentions('spicelover'))
        old_count = get_user_unread_count('spicelover')
        send_channel_message('arrakis', 1, 'Paul', '@spicelover', '2001-01-01')
        new_count = get_user_unread_count('spicelover')
        self.assertEqual(1, count_mentions('spicelover'))
        self.assertEqual(old_count + 1, new_count)
        conn.close()

    def test_s_get_mentions(self):
        conn = connect()
        self.assertEqual(1, count_mentions('spicelover'))
        send_channel_message('comedy', 1, 'Moe', '@spicelover', '2001-01-01')
        self.assertEqual(1, count_mentions('spicelover'))
        conn.close()

    def test_t_paul_suspended(self):
        conn = connect()
        send_channel_message('arrakis', 2, 'Paul', 'ooooohhhhh', '2010-01-01')
        suspend('Paul', 'arrakis')
        send_channel_message('arrakis', 2, 'Paul', 'AAAHHH', '2010-01-01')
        join_community(9, 'Paul', 'comedy')
        send_channel_message('comedy', 2, 'Paul', 'AAAHHH', '2010-01-01')
        conn.close()

    def test_u_paul_moe_dms(self):
        result = len(get_messages_between_users('Paul', 'Moe'))
        self.assertEqual(3, result)
        print(str(result), 'direct messages between Paul and Moe')

    def test_v_search_keyword(self):
        send_channel_message('comedy', 2, 'Larry', 'please reply', '2001-01-01')
        send_channel_message('comedy', 2, 'Larry', 'i replyed already!', '2001-01-01')
        messages = search_keyword('comedy', 'reply')
        for x in messages:
            print(x[0])
        messages = search_keyword('comedy', 'reply please')
        for x in messages:
            print(x[0])

    def test_w_moderator_query(self):
        users = moderator_query('arrakis', '2009-01-01', '2011-01-01', '2020-01-01')
        for x in users:
            print(x, 'is suspended from arrakis')

    def test_x_activity_summary(self):
        send_channel_message('comedy', 1, 'Paul', 'hi im paul', '2001-01-15')
        send_channel_message('comedy', 1, 'Abbott', 'hellooooo', '2001-01-15')
        send_channel_message('arrakis', 1, 'spicelover', 'i love spice', '2001-01-03')
        activity_summary('2001-01-20')
