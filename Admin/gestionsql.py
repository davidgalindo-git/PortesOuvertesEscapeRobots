import mysql.connector
import random

def open_db():
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            port='3306',
            user='root',
            password='root',
            database="groups_po"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Erreur de connexion : {err}")
        return None

def create_group(group_name):
    conn = open_db()
    if conn is None:
        return

    try:
        cursor = conn.cursor()

        # Générer les fragments
        caracteres = list("qwertzuiopasdfghjklyxcvbnm")
        frag1 = "".join(random.choices(caracteres, k=3))
        frag2 = "".join(random.choices(caracteres, k=3))
        frag3 = "".join(random.choices(caracteres, k=3))
        code = frag1 + frag2 + frag3

        print(f"Code généré : {code}")

        # Insertion du groupe
        sql = "INSERT INTO `groups` (group_name, code) VALUES (%s, %s)"
        cursor.execute(sql, (group_name, code))
        conn.commit()

        # Récupérer l'ID du groupe inséré
        cursor.execute("SELECT id FROM `groups` WHERE group_name = %s", (group_name,))
        result = cursor.fetchone()
        if result is None:
            print("Le groupe n’a pas été trouvé après insertion.")
            return
        group_id = result[0]

        # Insertion des fragments
        cursor.execute("INSERT INTO `fragment1` (id_group, frag) VALUES (%s, %s)", (group_id, frag1))
        cursor.execute("INSERT INTO `fragment2` (id_group, frag) VALUES (%s, %s)", (group_id, frag2))
        cursor.execute("INSERT INTO `fragment3` (id_group, frag) VALUES (%s, %s)", (group_id, frag3))
        conn.commit()

        print("Groupe et fragments créés avec succès.")

    except mysql.connector.Error as err:
        print(f"Erreur SQL : {err}")
    finally:
        cursor.close()
        conn.close()

def read_data():
    conn = open_db()

    cursor = conn.cursor()

    sql = "SELECT * FROM `groups`"
    cursor.execute(sql)
    return cursor.fetchall()

def identification(identity):
    conn = open_db()
    cursor = conn.cursor()
    sql = "SELECT id FROM `groups` WHERE `group_name` = %s"
    cursor.execute(sql, (identity,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None


def recuperation_frag(groupe_id, fragment):
    conn = open_db()
    cursor = conn.cursor()

    sql = f"SELECT frag FROM {fragment} WHERE id_group = %s"
    cursor.execute(sql, (groupe_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def recuperation_score(groupe_id):
    conn = open_db()
    cursor = conn.cursor()

    sql = f"SELECT score FROM `groups` WHERE id = %s"
    cursor.execute(sql, (groupe_id))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def new_score(groupe_id, score):
    conn = open_db()
    cursor = conn.cursor()

    sql = (f"UPDATE `groups` SET `score` = {score}, `date_score` = NOW() WHERE id = {groupe_id};")
    cursor.execute(sql, (groupe_id))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

