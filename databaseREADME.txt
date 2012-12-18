#######
Database keys:
key | value

Main Database (DB1):
user:<username> - userID
user:<userID> - ##Hash##
              - username
              - hashed password

user:<userID>:msgs -##Hash
              - 'unread' - list of unread messages (listed by msgNum value)
              - 'totalMsgs' - number of messages
              - messages by message number (<msgnumber> = message

        ###Message Format###
        (sender | timestamp | message | flags)
        <sender>userID1<time>timeInt<msg>Message (escape sequence is: !!00!! )



Session Database (DB2):#Keys are set to expire after 300 seconds
<UID>            - sessionID
<sessionID>      - UID
