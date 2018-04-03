import os
from prettytable import PrettyTable
from collections import defaultdict
import unittest

class Repository:
    
    def __init__(self, directory, prettytable = False):
        """Each file from the directory is read into its respective default dictionary and stored here
            The key is the CWID, and the corresponding information is the value"""
        self.students = dict() # key: CWID value: instance of class Student
        self.instructors = dict() # key: CWID value: instance of class Instructor
        try:
            os.chdir(directory)
        except FileNotFoundError:
            raise NotADirectoryError("Invalid Directory ({}). Please try again.".format(directory))
        else:
            student_path = os.path.join(directory, "students.txt")
            instructor_path = os.path.join(directory, "instructors.txt")
            grades_path = os.path.join(directory, "grades.txt")
            self.open_file_stud(student_path, '\t')
            self.open_file_inst(instructor_path, '\t')
            self.open_file_grades(grades_path, '\t')
        if prettytable == True:
            self.print_pretty_table_stud()
            self.print_pretty_table_inst()
    
    def open_file_stud(self, file, split_type = '\t'):
        """Opens a student.txt file and adds that information to a dictionary containing students
            Key: CWID, Value: Student(cwid, name, major)
            The dictionary will contain every student from the file after this function is called
            Raises a FileNotFoundError if the file cannot be found (ie. student.txt)
            Raises a ValueError if the file is not properly split"""
        expected_tokens = 3         #number of items expected in each line of student file
        try:
            fp = open(file, 'r')                             
        except FileNotFoundError:
            raise FileNotFoundError("Invalid File ({}). Please try again.".format(file))
        else:
            with fp:
                for line in fp:
                    line = line.strip().split(split_type)
                    if len(line) == expected_tokens:
                        cwid, name, major = line
                    else:
                        raise ValueError("Students must have the parameters CWID, Name, Major and split with {}".format(split_type))
                    self.students[cwid] = Student(cwid, name, major)

    def open_file_inst(self, file, split_type = '\t'):
        """Opens a instructor.txt file and adds that information to a dictionary containing instructors
            Key: CWID, Value: Instructor(cwid, name, department)
            The dictionary will contain every instructor from the file after this function is called
            Raises a FileNotFoundError if the file cannot be found (ie. instructor.txt)
            Raises a ValueError if the file is not properly split"""
        expected_tokens = 3         #number of items expected in each line of instructor file
        try:
            fp = open(file, 'r')                                
        except FileNotFoundError:
            raise FileNotFoundError("Invalid File ({}). Please try again.".format(file))
        else:
            with fp:
                for line in fp:
                    line = line.strip().split(split_type)
                    if len(line) == expected_tokens:
                        cwid, name, department = line
                    else:
                        raise ValueError("Instructors must have the parameters CWID, Name, Department and split with {}".format(split_type))
                    self.instructors[cwid] = Instructor(cwid, name, department)

    def open_file_grades(self, file, split_type = '\t'):
        """Opens a grade.txt file and adds that information to the dictionary containing students
            Key: CWID, Value: Student object
                Adds course name and grade to student if CWID is found in the student dictionary
                If CWID is not found, raises ValueError
            Also increases number of students in the course taught by the respective instructor
                If instructor's CWID is not found, raises ValueError""" 
        expected_tokens = 4
        try:
            fp = open(file, 'r')                          
        except FileNotFoundError:
            raise FileNotFoundError("Invalid File ({}). Please try again.".format(file))
        else:
            with fp:
                for line in fp:
                    line = line.strip().split(split_type)
                    if len(line) == expected_tokens:            #checks input from each line to makes sure it has 4 pieces of information
                        cwid, course, grade, teacher = line
                    else:
                        raise ValueError("Grades must have the parameters CWID, Course, Grade and Teacher and split with {}".format(split_type))
                    if cwid in self.students:                   #checks if the cwid has already been created as a student, if not raises error
                        self.students[cwid].add_course(course, grade)
                    else:
                        raise ValueError("Student with CWID: {} was never entered as a student".format(cwid))
                    if teacher in self.instructors:             #checks if the cwid of the teacher has been created as an instructor, if not raises error 
                        self.instructors[teacher].add_course(course)
                    else:
                        raise ValueError("Instructor with CWID: {} was never entered as an instructor".format(teacher))

    def print_pretty_table_stud(self):
        """Returns pretty table for student with table labels:
        CWID, Name, Courses (in sorted order)"""
        pt = PrettyTable(field_names = ['CWID', 'Name', 'Courses'])
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
    

class Student:
    
    def __init__(self, cwid, name, major):
        self.cwid = cwid    
        self.name = name
        self.major = major
        self.grades = defaultdict(str) #key: course, value: grade

    def add_course(self, course, grade):
        """Adds course grade to dictonary (key: course, value: grade)"""
        self.grades[course] = grade    

    def pretty_table_info(self):
        """Returns list of [cwid, name, [courses]-->(sorted list of courses)]"""
        return [self.cwid, self.name, sorted(self.grades.keys())]
       

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
    directory = r'\Users\TS\Desktop\Stevens\Work from Semesters\Fourth Semester\SSW 810\PycharmProjects\HW_9_Files'
    stevens = Repository(directory, True)
    

if __name__ == '__main__':
    main()
    