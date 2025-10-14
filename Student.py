################################################################################
class Student:
    ''' a class representing a Student data type, containing information
        pertinent for a typical Bates student '''
    __slots__ = ('_name', '_email', '_year', '_majors', '_minors', '_gecs', '_advisor')

    def __init__(self, name: str, email: str, year: str,  \
                 majors: list[str], minors: list[str], gecs: list[str],  \
                 advisor: str) -> None:
        ''' initializer method for a Student object, called implicitly when
            a new Student object is created
        Parameters:
            name:    (str) corresponding to the student's name, expected in
                            "Last, First" format
            email:   (str) student's email address
            year:    (int) student's year in college (1,2,3, or 4)
            majors:  (list[str]) a list of all declared majors for the student
            minors:  (list[str]) a list of all declared minors for the student
            gecs:    (list[str]) a list of all declared GECS for the student
            advisor: (str) name of the DCS advisor
        '''
        self._name    : str = name   # expected in Last, First format
        self._email   : str = email
        self._year    : int = year
        self._majors  : list[str] = majors
        self._minors  : list[str] = minors
        self._gecs    : list[str] = gecs
        self._advisor : str = advisor

    def __str__(self) -> str:
        ''' returns a string representation of the Student object '''
        # note the justification in printing, e.g.:
        #  {self._name:<24} left justifies self._name to a width of 24 chars
        return f"{self._name:<24}  {self._email:<18}  {self._year:<4}  " + \
               f"{','.join(self._majors):<15}  {','.join(self._minors):<10}  " + \
               f"{self._advisor}"
               #f"{','.join(self.gecs):<15}  {self.advisor}"

    def getCSVList(self) -> list[str]:
        ''' method to return the student info as a list
        Returns:
            a list of strings corresponding to info for the Student appropriate
            for eventual use when creating a CSV file
        '''
        names = self._name.split(', ')  # Last, First format
        return [names[0], names[1], self._email, str(self._year), \
                ",".join(self._majors), ",".join(self._minors), \
                ",".join(self._gecs), self._advisor]
    
################################################################################
def main() -> None:
    stu = Student("Foo, Abe", "afoo@bates.edu", 2024, ["MATH","BIOL"], \
                  ["DCS"], [""], "Shrout, Anelise")
    print(stu)
    csv_list = stu.getCSVList()
    lname    = csv_list[0]
    fname    = csv_list[1]
    advisor  = csv_list[-1]
    print(lname, fname, advisor)
    print(csv_list)

################################################################################
if __name__ == "__main__":
    main()
