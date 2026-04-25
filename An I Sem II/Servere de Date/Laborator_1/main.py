import oracledb

# conectare la server
conn = oracledb.connect(
    user="flavia_busnatu_bd",
    password="1234",
    host="193.231.20.20",
    port="15211",
    sid="orcl19c"
)

cursor = conn.cursor()

def afisare_tabele():
    print(f"\n--- TABELE ---")
    query = "SELECT table_name, tablespace_name FROM USER_ALL_TABLES"
    cursor.execute(query)
    for row in cursor:
        print(f"Table Name: {row[0]}, Tablespace Name: {row[1]}")

def afisare_tabel():
    nume_tabel = input("Introdu numele tabelului: ").upper()

    try:
        query = f"SELECT * FROM {nume_tabel}"
        cursor.execute(query)

        print(f"\n--- TABEL: {nume_tabel} ---")

        # numele coloanelor
        col_names = [col[0] for col in cursor.description]
        print(" | ".join(col_names))
        print("-" * 50)

        for row in cursor:
            print(" | ".join(str(x) for x in row))

    except Exception as e:
        print("Eroare:", e)

def afisare_view():
    print("\n--- VIEW PROCEDURI ---")
    cursor.execute("""
        SELECT object_name
        FROM view_procedures
    """)
    for row in cursor:
        print(row)

def executa_procedura():
    print("\n--- EXECUTIE PROCEDURA ---")
    p = int(input("Introdu procent (ex: 20): "))
    cursor.callproc("dbms_output.enable")
    cursor.callproc("PROCENT_TREATMENTS", [p])
    
    status = cursor.var(oracledb.NUMBER)
    line = cursor.var(oracledb.STRING)
    while True:
        cursor.callproc("dbms_output.get_line", [line, status])
        if status.getvalue() != 0:
            break
        print(line.getvalue())


while True:
    print("\n------ MENIU ------")
    print("1. Afisare tabele create de userul curent")
    print("2. Afisare date din tabel")
    print("3. Afisare view proceduri")
    print("4. Executare procedura cu procent")
    print("0. Iesire")

    optiune = input("Alege optiunea: ")

    if optiune == "2":
        afisare_tabel()
    elif optiune == "3":
        afisare_view()
    elif optiune == "4":
        executa_procedura()
    elif optiune == "1":
        afisare_tabele()
    elif optiune == "0":
        print("La revedere!")
        break
    else:
        print("Optiune invalida!")

cursor.close()
conn.close()
