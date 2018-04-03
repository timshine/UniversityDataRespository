import os
from prettytable import PrettyTable
from collections import defaultdict
import unittest

def open_file(file, expected_tokens, split_type = '\t'):
    """Open file generator. Can be used by any class in document."""
    try:
        fp = open(file, 'r')                             
    except FileNotFoundError:
        raise FileNotFoundError("Invalid File ({}). Please try again.".format(file))
    else:
        with fp:
            for line_number, line in enumerate(fp):
                line = line.strip().split(split_type)
                if len(line) == expected_tokens:
                    yield line
                else:
                    raise ValueError("There is an error in the format of line {}. Please refer to the proper formatting of the respective text file.".format(line_number))


class Repository:
    
    def __init__(self, directory, prettytable = False):
        """Each file from the directory is read into its respective default dictionary and stored here
            The key is the CWID, and the corresponding information is the value"""
        self.students = dict() # key: CWID value: instance of class Student
        self.instructors = dict() # key: CWID value: instance of class Instructor
        self.majors = dict() #key: department value: instance of Major
        try:
            os.chdir(directory)
        except FileNotFoundError:
            raise NotADirectoryError("Invalid Directory ({}). Please try again.".format(directory))
        else:
            #Sets appropriate path to text files
            student_path = os.path.join(directory, "students.txt")
            instructor_path = os.path.join(directory, "instructors.txt")
            grades_path = os.path.join(directory, "grades.txt")
            majors_path = os.path.join(directory, "majors.txt")
            #Opens the respective text files
            self.open_major_file(majors_path, '\t')
            self.open_stud_file(student_path, '\t')
            self.open_inst_file(instructor_path, '\t')
            self.open_grade_file(grades_path, '\t')
        if prettytable == True:
            print('Majors Summary')
            self.print_pretty_table_major()
            print('\nStudents Summary')
            self.print_pretty_table_stud()
            print('\nInstructors Summary')
            self.print_pretty_table_inst()
                    
    def open_stud_file(self, file, split_type):
        """Opens the student file and appends cwid, name, and major to the student dictionary"""
        expected_tokens = 3
        for cwid, name, department in open_file(file, expected_tokens,  '\t'):
            if department in self.majors: #checks to make sure the student is taking a major offered in the school
                self.students[cwid] = Student(cwid, name, department)
                self.students[cwid].enroll_major(self.majors[department])    #initializes the major for the student with required courses
            else:
                raise ValueError("The major {} is not offered at the university.".format(department))  

    def open_inst_file(self, file, split_type):
        """Opens the instructor file and appends cwid, name and department to instructor dictionary"""
        expected_tokens = 3
        for cwid, name, department in open_file(file, expected_tokens, '\t'):
            self.instructors[cwid] = Instructor(cwid, name, department)

    def open_grade_file(self, file, split_type):
        """Opens a grade.txt file and adds that information to the dictionary containing students
            Key: CWID, Value: Student object
                Adds course name and grade to student if CWID is found in the student dictionary
                If CWID is not found, raises ValueError
            Also increases number of students in the course taught by the respective instructor
                If instructor's CWID is not found, raises ValueError"""
        expected_tokens = 4
        for cwid, course, grade, teacher in open_file(file, expected_tokens, '\t'):
            if cwid in self.students:                   #checks if the cwid has already been created as a student, if not raises error
                self.students[cwid].add_course(course, grade)
            else:
                raise ValueError("Student with CWID: {} was never entered as a student".format(cwid))
            if teacher in self.instructors:             #checks if the cwid of the teacher has been created as an instructor, if not raises error 
                self.instructors[teacher].add_course(course)
            else:
                raise ValueError("Instructor with CWID: {} was never entered as an instructor".format(teacher))

    def open_major_file(self, file, split_type):
        """Opens major file and Major classes to the major dictionary in repository
            The major class holds more information about the major: required courses and elective courses"""
        expected_tokens = 3
        for major, flag, course_code in open_file(file, expected_tokens, '\t'):
            if major not in self.majors:
                self.majors[major] = Major(major)
            self.majors[major].add_course(course_code, flag)    #adds courses to the respective major
    
    def print_pretty_table_stud(self):
        """Returns pretty table for student with table labels:
        CWID, Name, Courses (in sorted order)"""
        pt = PrettyTable(field_names = ['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives'])
        for cwid in self.students:                     #prints out the list of files and information as a prettytable
            pt.add_row(self.students[cwid].pretty_table_info())
        print(pt)

    def print_pretty_table_inst(self):
        """Returns Pretty table for instructors with table labels:
        CWID, Name, Department, Course, Number of Students (in that respective course)"""
        pt = PrettyTable(field_names = ['CWID', 'Name', 'Department', 'Course', 'Number of Students'])
        for cwid in self.instructors:                     #prints out the list of files and information as a prettytable
            for course in self.instructors[cwid].pretty_table_info():
                pt.add_row(course)
        print(pt)

    def print_pretty_table_major(self):
        """Returns Pretty table for majors with table labels:
        Department, Required, Electives"""
        pt = PrettyTable(field_names = ['Dept.', 'Required', 'Electives'])
        for department in self.majors:                     #prints out the list of files and information as a prettytable
            pt.add_row(self.majors[department].pretty_table_info())
        print(pt)


class Major:
    
    def __init__(self, department):
        self.department = department
        self.required_courses = set()   #set of major required courses
        self.elective_courses = set()   #set of major elective courses

    def add_course(self, course_code, flag):
        """Adds courses to required_courses set and elective_courses set based on flag"""
        if flag.upper() == 'R':
            self.required_courses.add(course_code)
        elif flag.upper() == 'E':
            self.elective_courses.add(course_code)
        else:
            raise ValueError("The course {} is neither an elective or required course in the major".format(course_code))
    
    def pretty_table_info(self):
        """Returns list of [Department, Required Courses, Elective Courses]"""
        return [self.department, sorted(self.required_courses), sorted(self.elective_courses)]
        

class Student:
    
    def __init__(self, cwid, name, major):
        self.cwid = cwid    
        self.name = name
        self.major = major 
        self.taken_courses = defaultdict(str) #key: course, value: grade
        self.completed_courses = set()  #set of courses with passing grade
        self.remaining_required = set()   #set of remaining major required courses
        self.remaining_elective = set()   #set of remaining major elective courses

    def add_course(self, course_code, grade):
        """Adds course grade to dictonary (key: course, value: grade)"""
        self.taken_courses[course_code] = grade
        if grade in ['A+','A','A-','B+','B','B-','C+','C']:
            self.completed_courses.add(course_code)    
            self.remaining_required = self.remaining_required.difference(self.completed_courses)
            if len(self.remaining_elective.intersection(self.completed_courses)) > 0:
                self.remaining_elective = {None}
    
    def enroll_major(self, major):
        """Pairs the student with corresponding major class
            Takes in required classes and elective classes from major"""
        self.remaining_required = major.required_courses
        self.remaining_elective = major.elective_courses
        
    def pretty_table_info(self):
        """Returns list of [cwid, name, [courses]-->(sorted list of courses)]"""
        return [self.cwid, self.name, self.major, sorted(self.completed_courses), self.remaining_required, self.remaining_elective]


class Instructor:
    
    def __init__(self, cwid, name, department):
        self.cwid = cwid    
        self.name = name
        self.department = department
        self.courses = defaultdict(int) #key:couse name, value: number of students

    def add_course(self, course):
        """Adds one more student to a course that the instructor teaches"""
        self.courses[course] += 1

    def pretty_table_info(self):
        """Returns list of [cwid, name, department, course, number of students (in the course)]"""
        for course, num_stud in self.courses.items():
            yield [self.cwid, self.name, self.department, course, num_stud]


def main():
    """Prints pretty table for students and instructors"""
    directory = r'\Users\TS\Desktop\Stevens\Work from Semesters\Fourth Semester\SSW 810\PycharmProjects\HW_10_Data_Repository\Data_Repository_Files'
    stevens = Repository(directory, prettytable = True)

if __name__ == '__main__':
    main()
    