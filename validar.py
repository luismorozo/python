
#import tkinter as tk
#import mysql.connector
import psycopg2
from psycopg2 import Error
import sys
from tkinter import messagebox
def conectar():
    try:
        conexion = psycopg2.connect(user= 'postgres',
                          password = 'sinage',
                          host= '127.0.0.1' ,
                          port = '5432',
                          database= 'sinage')
        """conexion = mysql.connector.connect(
        host = 'localhost' ,
        user='root'   ,
        password= 'sinage',
        database='sinage'
        )"""
        
        return conexion
    except  Error as e:
        messagebox.showerror("Error,",str(e))

def validate_entry(text, new_text):
    if len(new_text) > 4:
        return False

    return text.isdecimal()

def btnsalir():
    sys.exit()

