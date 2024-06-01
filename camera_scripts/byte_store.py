import psycopg2
import cv2
import pickle

impath ="first_try/"

def setup_table(conn):
    conn.execute("create table blablub(id SERIAL, data bytea);")


def insert_data(desc, conn):
    conn.execute("INSERT into blablub(data) VALUES(%s)" %
                 psycopg2.Binary(pickle.dumps(desc)))


def load_images():
    with open(f"{impath}"):
        pass

def get_descriptors(orb, img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kp, des = orb.detectAndCompute(img, None)
    return des


def main():
    connection = psycopg2.connect(dbname="cem_testdb", user="cem",
                                  password="password", host="db.inftech.hs-mannheim.de", port="5432")
    setup_table()
    orb = cv2.ORB.create()
    get_descriptors(conn, orb)


if __name__ == "__main__":
    main()
