import unittest
import os
import Timothy_Shine_HW9
from Timothy_Shine_HW9 import Repository
from Timothy_Shine_HW9 import Student
from Timothy_Shine_HW9 import Instructor      
        
class StudentTest (unittest.TestCase):
    """Checks that the Student class is working properly"""

    def test_get_student_info(self):
        """Test the get_info method in Student
            This method should return a list of the student in the form [cwid, name, [sorted(courses)]]
            Student takes parameters (cwid, name, major)
            add_grades takes in parameters (course, letter_grade)"""
        joe = Student('12345', 'Joe Shmoe', 'SWEN')
        joe.add_course('SSW 810', 'A')
        joe.add_course('SYS 660', 'A')
        self.assertEqual(joe.pretty_table_info(), ['12345', 'Joe Shmoe', ['SSW 810','SYS 660']])


class InstructorTest (unittest.TestCase):
    """Checks that the Instructor class is working properly"""

    def test_get_instructor_info(self):
        """Test the get_info method in Instructor
            This method should return a list of the instructors in the form [cwid, name, department, course, students]
            Instructor takes parameters (cwid, name, department)
            add_course takes in parameter (course)"""
        alex = Instructor('98765', 'Alex Smith', 'SWEN')
        alex.add_course('SSW 810')
        alex.add_course('SYS 660')
        information = alex.pretty_table_info()
        self.assertEqual(next(information), ['98765', 'Alex Smith', 'SWEN', 'SSW 810', 1])
        self.assertEqual(next(information), ['98765', 'Alex Smith', 'SWEN', 'SYS 660', 1])


class RepositoryTest (unittest.TestCase):
    """Checks that the repository class is working correctly"""
    
    def test_good_input(self):
        """Tests some good input values and the corresponding results from each from the repository"""
        directory = r'\Users\TS\Desktop\Stevens\Work from Semesters\Fourth Semester\SSW 810\PycharmProjects\HW_9_Files'  #change this directory where the file is saved
        test_file = os.path.join(directory, 'Good_Test')
        student_test = {'10103': Student('10103', 'Baldwin,C', 'SFEN'), '10115': Student('10115', 'Wyatt, X', 'SFEN')}
        instructor_test = {'98765': Instructor('98765', 'Einstein, A', 'SFEN'), '98764': Instructor('98764', 'Feynman, R', 'SFEN')}
        self.assertTrue(student_test.keys() == Repository(test_file).students.keys())               #tests that students holds a dictionary with key:cwid and value: instance of student
        self.assertTrue(instructor_test.keys() == Repository(test_file).instructors.keys())         #tests that instructors holds a dictionary with key:cwid and value: instance of instructor
    
    def test_bad_input(self):
        """Tests all bad inputs and their corresponding Errors that they raise"""
        #ValueErrors:
        directory = r'\Users\TS\Desktop\Stevens\Work from Semesters\Fourth Semester\SSW 810\PycharmProjects\HW_9_Files'
        with self.assertRaises(ValueError):
            Repository(os.path.join(directory, "Bad_Student"))                  #doesn't contain proper format for a student
        with self.assertRaises(ValueError):    
            Repository(os.path.join(directory, "New_Student_from_grade"))       #has grades for someone who isn't a student
        #FileNotFoundErrors:
        with self.assertRaises(FileNotFoundError):    
            Repository(os.path.join(directory, "Folder_has_no_files"))          #this folder has no files
        with self.assertRaises(FileNotFoundError):
            test = Repository(directory)
            test.open_file_stud("not_a_real_file.txt")                          #file doesnt exist, open_file method does not work
        #NotADirectoryErrors:
        with self.assertRaises(NotADirectoryError):
            Repository(r'\This\will\not\work')                                  #Not a real directory
        with self.assertRaises(NotADirectoryError):    
            Repository(os.path.join(directory, "Not_A_Real_Folder"))            #this folder doesnt exist


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)