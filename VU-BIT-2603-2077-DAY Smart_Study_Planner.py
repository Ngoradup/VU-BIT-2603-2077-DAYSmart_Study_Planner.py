# ============================================================
# Smart Study Planner
# Individual Assignment
# ============================================================

FILE_NAME = "study_log.txt"


# ------------------------------------------------------------
# classify_session()
# Classifies a study session according to its duration.
# ------------------------------------------------------------
def classify_session(duration):
    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"


# ------------------------------------------------------------
# add_session()
# Allows the user to enter and store a new study session.
# ------------------------------------------------------------
def add_session(sessions):
    print("\n========== ADD STUDY SESSION ==========")

    subject = input("Enter subject name: ").strip()
    topic = input("Enter topic covered: ").strip()
    date = input("Enter date/day label: ").strip()

    # Keep asking until the user enters a positive number.
    while True:
        duration_input = input("Enter duration in minutes: ").strip()

        try:
            duration = float(duration_input)

            if duration > 0:
                break
            else:
                print("Duration must be a positive number.")

        except ValueError:
            print("Invalid input. Please enter a number.")

    session = {
        "subject": subject,
        "topic": topic,
        "date": date,
        "duration": duration
    }

    sessions.append(session)

    print("\nStudy session added successfully!")
    print(f"Classification: {classify_session(duration)}")


# ------------------------------------------------------------
# view_sessions()
# Displays all recorded study sessions in a table.
# ------------------------------------------------------------
def view_sessions(sessions):
    print("\n================ ALL STUDY SESSIONS ================")

    if not sessions:
        print("No study sessions have been recorded yet.")
        return

    print("-" * 85)
    print(
        f"{'No.':<5}"
        f"{'Subject':<20}"
        f"{'Topic':<25}"
        f"{'Date':<15}"
        f"{'Minutes':<10}"
        f"{'Class':<10}"
    )
    print("-" * 85)

    for index, session in enumerate(sessions, start=1):
        classification = classify_session(session["duration"])

        print(
            f"{index:<5}"
            f"{session['subject']:<20}"
            f"{session['topic']:<25}"
            f"{session['date']:<15}"
            f"{session['duration']:<10.1f}"
            f"{classification:<10}"
        )

    print("-" * 85)


# ------------------------------------------------------------
# search_by_subject()
# Searches for sessions belonging to a particular subject.
# The search is case-insensitive.
# ------------------------------------------------------------
def search_by_subject(sessions):
    print("\n========== SEARCH BY SUBJECT ==========")

    subject = input("Enter subject to search: ").strip()

    found_sessions = []

    for session in sessions:
        if session["subject"].lower() == subject.lower():
            found_sessions.append(session)

    if not found_sessions:
        print(f"\nNo study sessions found for '{subject}'.")
        return

    print(f"\nStudy sessions for: {subject}")
    print("-" * 80)

    print(
        f"{'No.':<5}"
        f"{'Topic':<30}"
        f"{'Date':<15}"
        f"{'Minutes':<12}"
        f"{'Class':<10}"
    )

    print("-" * 80)

    total_minutes = 0

    for index, session in enumerate(found_sessions, start=1):
        classification = classify_session(session["duration"])
        total_minutes += session["duration"]

        print(
            f"{index:<5}"
            f"{session['topic']:<30}"
            f"{session['date']:<15}"
            f"{session['duration']:<12.1f}"
            f"{classification:<10}"
        )

    print("-" * 80)
    print(f"Total time spent on {subject}: {total_minutes / 60:.2f} hours")


# ------------------------------------------------------------
# study_statistics()
# Calculates overall and subject-based study statistics.
# ------------------------------------------------------------
def study_statistics(sessions):
    print("\n========== STUDY STATISTICS ==========")

    if not sessions:
        print("No study sessions available for statistics.")
        return

    # Calculate total study time.
    total_minutes = sum(session["duration"] for session in sessions)
    total_hours = total_minutes / 60

    print(f"\nTotal hours studied overall: {total_hours:.2f} hours")

    # Calculate study time for each subject.
    subject_totals = {}

    for session in sessions:
        subject = session["subject"]

        if subject not in subject_totals:
            subject_totals[subject] = 0

        subject_totals[subject] += session["duration"]

    print("\nTotal hours studied per subject:")
    print("-" * 40)

    for subject, minutes in subject_totals.items():
        print(f"{subject:<25} {minutes / 60:.2f} hours")

    # Find the subject with the least study time.
    weakest_subject = min(subject_totals, key=subject_totals.get)
    weakest_time = subject_totals[weakest_subject]

    print("\nWeakest study area:")
    print(
        f"{weakest_subject} "
        f"({weakest_time / 60:.2f} hours)"
    )

    # Find the longest individual study session.
    longest_session = max(sessions, key=lambda session: session["duration"])

    print("\nLongest study session:")
    print(f"Subject: {longest_session['subject']}")
    print(f"Topic: {longest_session['topic']}")
    print(f"Date: {longest_session['date']}")
    print(f"Duration: {longest_session['duration']:.1f} minutes")
    print(
        f"Classification: "
        f"{classify_session(longest_session['duration'])}"
    )


# ------------------------------------------------------------
# save_sessions()
# Saves all sessions to study_log.txt.
# ------------------------------------------------------------
def save_sessions(sessions):
    try:
        with open(FILE_NAME, "w") as file:

            for session in sessions:
                # Each session is stored on one line.
                file.write(
                    f"{session['subject']}|"
                    f"{session['topic']}|"
                    f"{session['date']}|"
                    f"{session['duration']}\n"
                )

        print("\nStudy sessions saved successfully.")

    except OSError as error:
        print(f"Error saving study sessions: {error}")


# ------------------------------------------------------------
# load_sessions()
# Loads existing sessions from study_log.txt.
# ------------------------------------------------------------
def load_sessions():
    sessions = []

    try:
        with open(FILE_NAME, "r") as file:

            for line in file:
                line = line.strip()

                if not line:
                    continue

                parts = line.split("|")

                # Check that the stored record has all required fields.
                if len(parts) == 4:
                    subject = parts[0]
                    topic = parts[1]
                    date = parts[2]

                    try:
                        duration = float(parts[3])

                        session = {
                            "subject": subject,
                            "topic": topic,
                            "date": date,
                            "duration": duration
                        }

                        sessions.append(session)

                    except ValueError:
                        # Ignore damaged duration records.
                        continue

    except FileNotFoundError:
        # This is normal during the first run.
        sessions = []

    except OSError as error:
        print(f"Error loading study sessions: {error}")

    return sessions


# ------------------------------------------------------------
# display_menu()
# Displays the main menu.
# ------------------------------------------------------------
def display_menu():
    print("\n")
    print("=" * 50)
    print("           SMART STUDY PLANNER")
    print("=" * 50)
    print("1. Add a study session")
    print("2. View all sessions")
    print("3. Search sessions by subject")
    print("4. View statistics")
    print("5. Save and exit")
    print("=" * 50)


# ------------------------------------------------------------
# main()
# Controls the entire programme.
# ------------------------------------------------------------
def main():

    # Load previous sessions when the programme starts.
    sessions = load_sessions()

    print("\nWelcome to the Smart Study Planner!")

    if sessions:
        print(f"{len(sessions)} previous session(s) loaded.")
    else:
        print("No previous sessions found. Starting a new study log.")

    while True:

        display_menu()

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_session(sessions)

        elif choice == "2":
            view_sessions(sessions)

        elif choice == "3":
            search_by_subject(sessions)

        elif choice == "4":
            study_statistics(sessions)

        elif choice == "5":
            save_sessions(sessions)
            print("Thank you for using the Smart Study Planner!")
            print("Goodbye!")
            break

        else:
            print("\nInvalid menu choice.")
            print("Please enter a number from 1 to 5.")


# ------------------------------------------------------------
# Programme entry point
# ------------------------------------------------------------
if __name__ == "__main__":
    main()