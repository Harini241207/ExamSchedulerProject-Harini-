from flask import Flask, render_template, request

from scheduler import generate_exam_dates
from scheduler import generate_schedule

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():

    # ====================================
    # FIRST PAGE LOAD
    # ====================================

    if request.method == 'GET':
        return render_template('index.html')

    # ====================================
    # STORE BRANCHES
    # ====================================

    branches = {}

    num_branches = int(
        request.form['numBranches']
    )

    for i in range(1, num_branches + 1):

        branch_name = request.form.get(
            f'branch{i}'
        )

        students = int(
            request.form.get(
                f'students{i}'
            )
        )

        branches[branch_name] = students

    print("\nBRANCHES:")
    print(branches)

    # ====================================
    # STORE SUBJECTS
    # ====================================

    subjects = {}

    for branch_count in range(1, num_branches + 1):

        num_subjects = request.form.get(
            f'subjects{branch_count}'
        )

        if num_subjects:

            num_subjects = int(num_subjects)

            for s in range(1, num_subjects + 1):

                subject_name = request.form.get(
                    f'subject_{branch_count}_{s}'
                )

                branch_list = []

                for b in range(1, branch_count + 1):

                    branch = request.form.get(
                        f'subject_{branch_count}_{s}_branch{b}'
                    )

                    branch_list.append(branch)

                subjects[subject_name] = branch_list

    print("\nSUBJECTS:")
    print(subjects)

    # ====================================
    # STORE CLASSROOMS
    # ====================================

    rooms = {}

    num_rooms = int(
        request.form['num_classrooms']
    )

    capacity = int(
        request.form['capacity']
    )

    for r in range(1, num_rooms + 1):

        rooms[f'Room{r}'] = capacity

    print("\nROOMS:")
    print(rooms)

    # ====================================
    # STORE START DATE
    # ====================================

    start_date = request.form['startdate']

    print("\nSTART DATE:")
    print(start_date)

    # ====================================
    # GENERATE EXAM DATES
    # ====================================

    exam_dates = generate_exam_dates(
        start_date,
        10
    )

    print("\nEXAM DATES:")

    for exam in exam_dates:

        print(
            exam['date'],
            exam['day']
        )

    # ====================================
    # GENERATE FINAL SCHEDULE
    # ====================================

    final_schedule = generate_schedule(
        subjects,
        branches,
        rooms,
        exam_dates
    )

    print("\nFINAL SCHEDULE:")
    print(final_schedule)

    # ====================================
    # SEND TO HTML
    # ====================================

    return render_template(
        'index.html',
        schedule=final_schedule
    )


if __name__ == '__main__':
    app.run(debug=True)