
import re
import sqlite3
from datetime import date

DB_NAME = "heavytech.db"


def initialize_database(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT NOT NULL,
            serial_number TEXT NOT NULL,
            service_date TEXT NOT NULL,
            engine_hours INTEGER NOT NULL,
            last_service_hours INTEGER NOT NULL,
            service_interval INTEGER NOT NULL,
            next_service INTEGER NOT NULL,
            hours_remaining INTEGER NOT NULL,
            status TEXT NOT NULL,
            problem TEXT NOT NULL,
            priority TEXT NOT NULL,
            recommendation TEXT NOT NULL,
            urgency TEXT NOT NULL
        )
    """)
    connection.commit()


def read_nonnegative_int(prompt):
    while True:
        try:
            value = int(input(prompt))

            if value < 0:
                print("ERROR: Value cannot be negative.")
            else:
                return value

        except ValueError:
            print("ERROR: Enter a whole number.")


def get_service_interval(model):
    match = re.search(r"\d+", model)

    if not match:
        return None

    model_number = int(match.group())

    if model_number < 75:
        return 250

    return 500


def print_report(report):
    print()
    print("=" * 35)
    print("       HEAVYTECH SERVICE REPORT")
    print("=" * 35)
    print("Report ID:", report["id"])
    print("Machine:", report["model"])
    print("Serial number:", report["serial_number"])
    print("Service date:", report["service_date"])
    print("Engine hours:", report["engine_hours"])
    print("Last service hours:", report["last_service_hours"])
    print("Service interval:", report["service_interval"])
    print("Next service:", report["next_service"])
    print("Hours remaining:", report["hours_remaining"])
    print("Status:", report["status"])
    print("Reported problem:", report["problem"])
    print("Problem priority:", report["priority"])
    print("Recommendation:", report["recommendation"])
    print("Overall urgency:", report["urgency"])
    print("=" * 35)


def create_report(connection):
    print()
    print("===== CREATE SERVICE REPORT =====")

    while True:
        model = input("Enter machine model: ").strip()
        service_interval = get_service_interval(model)

        if model and service_interval is not None:
            break

        print("ERROR: Enter a valid model containing a number.")

    while True:
        serial_number = input("Enter serial number: ").strip()

        if serial_number:
            break

        print("ERROR: Serial number cannot be empty.")

    engine_hours = read_nonnegative_int("Enter engine hours: ")

    while True:
        last_service_hours = read_nonnegative_int(
            "Last service hours (0 if unknown/not recorded): "
        )

        if last_service_hours <= engine_hours:
            break

        print("ERROR: Last service hours cannot exceed current engine hours.")

    problem = input("Enter problem: ").strip()

    if not problem:
        problem = "Not specified"

    while True:
        priority = input("Enter priority (High/Medium/Low): ").strip().capitalize()

        if priority in ("High", "Medium", "Low"):
            break

        print("ERROR: Enter High, Medium or Low.")

    if last_service_hours == 0:
        next_service = 50
    else:
        next_service = (
            last_service_hours // service_interval + 1
        ) * service_interval

    hours_remaining = next_service - engine_hours

    if hours_remaining < 0:
        status = "Service overdue"
    elif hours_remaining <= 50:
        status = "Service warning!"
    else:
        status = "Service is not due soon."

    if priority == "High":
        recommendation = "Urgent inspection required."
    elif priority == "Medium":
        recommendation = "Inspection should be scheduled."
    else:
        recommendation = "Inspect during next planned service."

    if priority == "High":
        urgency = "Critical"
    elif status == "Service overdue":
        urgency = "High"
    elif priority == "Medium" or status == "Service warning!":
        urgency = "Medium"
    else:
        urgency = "Low"

    service_date = date.today().isoformat()

    cursor = connection.execute("""
        INSERT INTO reports (
            model, serial_number, service_date,
            engine_hours, last_service_hours,
            service_interval, next_service, hours_remaining,
            status, problem, priority, recommendation, urgency
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        model, serial_number, service_date,
        engine_hours, last_service_hours,
        service_interval, next_service, hours_remaining,
        status, problem, priority, recommendation, urgency
    ))

    connection.commit()

    report = connection.execute(
        "SELECT * FROM reports WHERE id = ?",
        (cursor.lastrowid,)
    ).fetchone()

    print()
    print("Service report saved successfully!")
    print_report(report)


def search_by_serial_number(connection):
    serial_number = input("Enter serial number: ").strip()

    if not serial_number:
        print("Serial number cannot be empty.")
        return

    report = connection.execute("""
        SELECT * FROM reports
        WHERE LOWER(serial_number) = LOWER(?)
        ORDER BY engine_hours DESC, id DESC
        LIMIT 1
    """, (serial_number,)).fetchone()

    if report:
        print_report(report)
    else:
        print("Machine not found!")


def show_service_history(connection):
    serial_number = input("Enter serial number: ").strip()

    if not serial_number:
        print("Serial number cannot be empty.")
        return

    reports = connection.execute("""
        SELECT * FROM reports
        WHERE LOWER(serial_number) = LOWER(?)
        ORDER BY engine_hours ASC, id ASC
    """, (serial_number,)).fetchall()

    if not reports:
        print("No service history found for this machine!")
        return

    print()
    print("===== SERVICE HISTORY =====")

    for report in reports:
        print_report(report)


def search_by_problem(connection):
    keyword = input("Enter problem keyword: ").strip()

    if not keyword:
        print("Keyword cannot be empty.")
        return

    reports = connection.execute("""
        SELECT * FROM reports
        WHERE LOWER(problem) LIKE LOWER(?)
        ORDER BY service_date DESC, id DESC
    """, (f"%{keyword}%",)).fetchall()

    if not reports:
        print("No matching problems found!")
        return

    print()
    print("===== MATCHING REPORTS =====")

    for report in reports:
        print_report(report)


def main():
    with sqlite3.connect(DB_NAME) as connection:
        connection.row_factory = sqlite3.Row
        initialize_database(connection)

        while True:
            print()
            print("===== HeavyTech Diagnostics =====")
            print("1. Create service report")
            print("2. Search by serial number")
            print("3. Show service history")
            print("4. Search by problem")
            print("5. Exit")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                create_report(connection)
            elif choice == "2":
                search_by_serial_number(connection)
            elif choice == "3":
                show_service_history(connection)
            elif choice == "4":
                search_by_problem(connection)
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Enter 1, 2, 3, 4 or 5.")


if __name__ == "__main__":
    main()
