from datetime import datetime, timedelta


# ==========================================
# GENERATE EXAM DATES
# ==========================================

def generate_exam_dates(start_date, total_days):

    exam_dates = []

    current_date = datetime.strptime(
        start_date,
        "%Y-%m-%d"
    )

    while len(exam_dates) < total_days:

        # Sunday = 6

        if current_date.weekday() != 6:

            exam_dates.append({

                "date":
                current_date.strftime("%Y-%m-%d"),

                "day":
                current_date.strftime("%A")

            })

        current_date += timedelta(days=1)

    return exam_dates


# ==========================================
# CHECK CLASH
# ==========================================

def has_clash(subject1_branches, subject2_branches):

    # Convert both lists into sets

    set1 = set(subject1_branches)
    set2 = set(subject2_branches)

    # Find common branches

    common = set1.intersection(set2)

    # If common branches exist

    if common:
        return True

    # No clash

    return False


# ==========================================
# ROOM ALLOCATION
# ==========================================

def allocate_branch_rooms(branch_students, rooms):

    allocation = {}

    # IMPORTANT:
    # DO NOT COPY
    # because rooms should remain occupied
    # throughout the same day

    remaining_capacity = rooms

    for branch, students in branch_students.items():

        remaining_students = students

        # ======================================
        # TRY SINGLE ROOM FIRST
        # ======================================

        for room, capacity in remaining_capacity.items():

            if students <= capacity:

                if room not in allocation:
                    allocation[room] = []

                allocation[room].append(
                    f"{students} {branch}"
                )

                remaining_capacity[room] -= students

                remaining_students = 0

                break

        # ======================================
        # SPLIT IF NEEDED
        # ======================================

        if remaining_students > 0:

            for room, capacity in remaining_capacity.items():

                if remaining_students <= 0:
                    break

                if capacity > 0:

                    assigned = min(
                        remaining_students,
                        capacity
                    )

                    if room not in allocation:
                        allocation[room] = []

                    allocation[room].append(
                        f"{assigned} {branch}"
                    )

                    remaining_capacity[room] -= assigned

                    remaining_students -= assigned

    return allocation


# ==========================================
# CREATE EMPTY SCHEDULE
# ==========================================

def create_empty_schedule(exam_dates):

    schedule = {}

    for exam in exam_dates:

        day_name = exam['date']

        schedule[day_name] = []

    return schedule


# ==========================================
# MAIN SCHEDULING FUNCTION
# ==========================================

def generate_schedule(
        subjects,
        branches,
        rooms,
        exam_dates
):

    # ======================================
    # CREATE EMPTY SCHEDULE
    # ======================================

    schedule = create_empty_schedule(
        exam_dates
    )

    # ======================================
    # TRACK ROOM USAGE DAY-WISE
    # ======================================

    day_room_usage = {}

    for day in schedule:

        day_room_usage[day] = rooms.copy()

    # ======================================
    # LOOP THROUGH SUBJECTS
    # ======================================

    for subject, subject_branches in subjects.items():

        placed = False

        # ======================================
        # CALCULATE TOTAL STUDENTS
        # ======================================

        total_students = 0

        branch_students = {}

        for branch in subject_branches:

            students = branches[branch]

            branch_students[branch] = students

            total_students += students

        # ======================================
        # TRY EACH DAY
        # ======================================

        for day in schedule:

            clash_found = False

            # ==================================
            # CHECK REMAINING DAY CAPACITY
            # ==================================

            remaining_day_capacity = sum(
                day_room_usage[day].values()
            )

            if total_students > remaining_day_capacity:
                continue

            # ==================================
            # CHECK EXISTING EXAMS
            # ==================================

            for scheduled_exam in schedule[day]:

                existing_subject = scheduled_exam[
                    "subject"
                ]

                existing_branches = subjects[
                    existing_subject
                ]

                # CHECK CLASH

                if has_clash(
                    subject_branches,
                    existing_branches
                ):

                    clash_found = True
                    break

            # ==================================
            # IF NO CLASH → SCHEDULE EXAM
            # ==================================

            if not clash_found:

                room_allocation = allocate_branch_rooms(
                    branch_students,
                    day_room_usage[day]
                )

                schedule[day].append({

                    "subject": subject,

                    "branches": subject_branches,

                    "students": total_students,

                    "rooms": room_allocation

                })

                placed = True

                break

        # ======================================
        # IF SUBJECT COULD NOT BE PLACED
        # ======================================

        if not placed:

            print(
                f"Could not place {subject}"
            )

    return schedule