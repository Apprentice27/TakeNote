import sqlite3

connection = sqlite3.connect('database.db')

crsr = connection.cursor()

all_files_and_titles = []

update_file = False


def createTable():
    """
    This function creates the database table

    :return:
    """
    crsr.execute("CREATE TABLE IF NOT EXISTS SavedFiles(title TEXT, file_data TEXT)")


def closeDataBase():
    """
    This function closes the database

    :return:
    """
    crsr.close()
    connection.close()


def createNewFile(f_title, f_data):
    crsr.execute("INSERT INTO SavedFiles (title, file_data) VALUES (?, ?)", (f_title, f_data))
    connection.commit()


def updateFile(f_title, f_data):
    crsr.execute("UPDATE SavedFiles set file_data = ? where title = ?", (f_data, f_title))
    connection.commit()


def saveFilesToList():
    """
    This function saves all the files to the files_and_titles

    :return:
    """
    global all_files_and_titles

    del all_files_and_titles[:]

    crsr.execute("SELECT title, file_data FROM SavedFiles")
    for row in crsr.fetchall():
        all_files_and_titles.append(list(row))

    for i in all_files_and_titles:
        print(i)


def updateDataBase(recent_title, recent_file_data):
    """
    This function updates the database with the new file given

    :param recent_title:
    :param recent_file_data:
    :return:
    """

    global all_files_and_titles
    global update_file

    for file in all_files_and_titles:
        if file[0] == recent_title:
            print('UPDATING FILE')
            update_file = True

    if not update_file:
        createNewFile(recent_title, recent_file_data)
        # return 'new file'
    elif update_file:
        updateFile(recent_title, recent_file_data)
        # return 'updated file'

    saveFilesToList()
    print(all_files_and_titles)


def permissionToCreateButton():
    if not update_file:
        return True
    elif update_file:
        return False


def getFileData(f_title):
    crsr.execute("SELECT title, file_data FROM SavedFiles")
    for row in crsr.fetchall():
        print(row)
        if row[0] == f_title:
            return row[1]


def getLastFile():
    """
    This function gets the last file of the files_and_titles list which is also known as the recently saved file

    :return:
    """

    return all_files_and_titles[-1]

# files_and_titles = []
#
# for i in range(len(titles)):
#     holder = []
#     holder.append(titles[i])
#     holder.append(files[i])
#     files_and_titles.append(holder)
#
# print(files_and_titles)
#
#
# for item in files_and_titles:
#     print(item[0])
#
# for item in files_and_titles:
#     print(item[1])
#

# gets all the data in the database and stores it into the all_files_and_titles list
