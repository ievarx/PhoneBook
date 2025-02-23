import os

# تحقق من وجود مكتبة معينة وإذا لم تكن موجودة قم بتثبيتها
try:
    import mysql.connector
except ImportError:
    print("Installing mysql-connector-python...")
    os.system('pip install mysql-connector-python')

try:
    import kivy
except ImportError:
    print("Installing kivy...")
    os.system('pip install kivy')
