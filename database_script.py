import sqlite3
db_name = 'quiz.sqlite'
conn = None
cursor = None

# create a connection to database
def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

#create query function
def do(query):
    cursor.execute(query)
    conn.commit()

# Before create anything, make sure we reset everything
def clear_db():
    open()
    query1 = '''DROP TABLE IF EXISTS quiz_content'''
    query2 = '''DROP TABLE IF EXISTS questions'''
    query3 = '''DROP TABLE IF EXISTS quiz'''
    do(query1)
    do(query2)
    do(query3)
    close()

def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    quiz_table = '''
    CREATE TABLE IF NOT EXISTS quiz(
    id INTEGER PRIMARY KEY, 
    name VARCHAR
    )
    '''
    question_table = '''
        CREATE TABLE IF NOT EXISTS questions(  
        id  INTEGER PRIMARY KEY, 
        question    VARCHAR,
        answer      VARCHAR,
        wrong1      VARCHAR,
        wrong2     VARCHAR,
        wrong3    VARCHAR
        )
        '''

    quiz_content_table = '''
        CREATE TABLE IF NOT EXISTS quiz_content(
        id          INTEGER     PRIMARY KEY, 
        quiz_id     INTEGER,
        question_id INTEGER,
        FOREIGN KEY(quiz_id) REFERENCES quiz(id),
        FOREIGN KEY (question_id) REFERENCES questions(id)
        )
    '''

    do(quiz_table)
    do(question_table)
    do(quiz_content_table)

    close()

def add_questions():
    questions = [
    ('Who is considered the founding father of sociology?', 'Auguste Comte', 'Karl Marx', 'Max Weber', 'Emile Durkheim'),
    ('Which term describes the process by which individuals learn the norms and values of their society?', 'Socialization', 'Assimilation', 'Stratification', 'Segregation'),
    ('What concept refers to a shared set of values, beliefs, and behaviors in a group?', 'Culture', 'Institutions', 'Bureaucracy', 'Demographics'),
    ('What is the term for a societal structure where social positions are ranked in a hierarchy?', 'Social Stratification', 'Social Mobility', 'Social Cohesion', 'Social Norms'),
    ('What is the largest ocean on Earth by surface area?', 'Pacific Ocean', 'Atlantic Ocean', 'Indian Ocean', 'Arctic Ocean'),
    ('Which mountain range acts as a natural border between Europe and Asia?', 'Ural Mountains', 'Alps', 'Andes', 'Himalayas'),
    ('What is the capital city of Australia?', 'Canberra', 'Sydney', 'Melbourne', 'Brisbane'),
    ('Which river is the longest in the world?', 'Nile River', 'Amazon River', 'Mississippi River', 'Yangtze River'),
    ('What is the value of 7 squared?', '49', '42', '56', '36'),
    ('What is the perimeter of a rectangle with length 8 units and width 5 units?', '26', '40', '13', '30'),
    ('What is the value of x if 2x + 6 = 14?', '4', '3', '5', '8'),
    ('What is 20 percent of 150?', '30', '25', '35', '20')
    ]
    open()
    cursor.executemany('''INSERT INTO questions(question, answer, wrong1, wrong2, wrong3) VALUES (?,?,?,?,?)''', questions)
    conn.commit()
    close()


def add_quiz(): #function to create quiz category
    quizes = [
        ('Sociology',),
        ('Geography',),
        ('Maths',)
    ]
    open()
    cursor.executemany('''INSERT INTO quiz(name)VALUES (?)''', quizes)
    conn.commit()
    close()

def add_links(): # create relation between question and its category
    link = [
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 5),
        (2, 6),
        (2, 7),
        (2, 8),
        (3, 9),
        (3, 10),
        (3, 11),
        (3, 12)
    ]
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    cursor.executemany('''INSERT INTO quiz_content(quiz_id, question_id) VALUES (?,?)''',link)
    conn.commit()
    close()
    print('Data seeded succesfully')

def get_question_after(question_id = 0, quiz_id=1):
    open()
    query ='''
    SELECT quiz_content.id,
            questions.question,
            questions.answer,
            questions.wrong1,
            questions.wrong2,
            questions.wrong3
        FROM questions, quiz_content
        WHERE quiz_content.question_id == questions.id
        AND quiz_content.id > ?
        AND quiz_content.quiz_id == ?
        ORDER BY quiz_content.id
    '''

    cursor.execute(query, [question_id, quiz_id])
    result = cursor.fetchone()
    close()
    return result

def get_quizes():
    query = 'SELECT * FROM quiz ORDER BY id'
    open()
    cursor.execute(query)
    result = cursor.fetchall()
    close()
    return result

def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall)
    close()

def show_table():
    show('questions')
    show('quiz')
    show('quiz_content')


def check_answer(q_id, ans_text):
  query = '''
    SELECT questions.answer
    FROM quiz_content, questions
    WHERE quiz_content.id = ?
    AND quiz_content.question_id = questions.id
  '''
  open()
  cursor.execute(query, (q_id,))
  result = cursor.fetchone()
  close()
  if result is None:
    return False
  else:
    if result[0] == ans_text:
      return True
    else:
      return False

def get_quiz_count():
    query = 'SELECT MAX(quiz_id) FROM quiz_content'
    open()
    cursor.execute(query)
    result = cursor.fetchone()
    close()
    return result

from random import randint
def get_random_quiz_id():
    query = 'SELECT quiz_id FROM quiz_content'
    open()
    cursor.execute(query)
    ids = cursor.fetchall()
    rand_num = randint(0, len(ids - 1))
    rand_id = ids[rand_num][0]
    close()
    return rand_id

def get_random_quiz_id():
    pass

def main():
    clear_db()
    create()
    add_questions()
    add_quiz()
    add_links()
    show_table()
    print(get_question_after(0, 1))

if __name__ == "__main__":
    main()