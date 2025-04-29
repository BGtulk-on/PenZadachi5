from abc import ABC, abstractmethod
import functools

def validate_data(func):
    @functools.wraps(func)
    def wrapper(instance, name, age, condition):
        if not isinstance(name, str) or not name:
            raise ValueError("Името трябва да бъде непразен низ.")
        if not isinstance(age, int) or age <= 0:
            raise ValueError("Възрастта трябва да бъде положително цяло число.")
        
        cls_name = instance.__class__.__name__
        if cls_name == "AdultPatient" and age < 18:
             raise ValueError("Възрастта на AdultPatient трябва да бъде 18 или повече.")
        if cls_name == "ChildPatient" and age >= 18:
             raise ValueError("Възрастта на ChildPatient трябва да бъде под 18.")
             
        return func(instance, name, age, condition)
    return wrapper

class Patient(ABC):
    def __init__(self, name: str, age: int, condition: str):
        self.name = name
        self.age = age
        self.condition = condition

    @abstractmethod
    def display_info(self):
        pass

class AdultPatient(Patient):
    @validate_data
    def __init__(self, name: str, age: int, condition: str):
        super().__init__(name, age, condition)

    def display_info(self):
        print(f"Adult Patient: {self.name}, Age: {self.age}, Condition: {self.condition}")

class ChildPatient(Patient):
    @validate_data
    def __init__(self, name: str, age: int, condition: str):
         super().__init__(name, age, condition)

    def display_info(self):
        print(f"Child Patient: {self.name}, Age: {self.age}, Condition: {self.condition}")

class PatientList:
    def __init__(self):
        self._patients = []
        self._index = 0

    def add_patient(self, patient: Patient):
        self._patients.append(patient)

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self._patients):
            result = self._patients[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration

    def adult_patients_generator(self):
        for patient in self._patients:
            if isinstance(patient, AdultPatient):
                yield patient

if __name__ == "__main__":
    try:
        p1 = AdultPatient("Иван Иванов", 30, "Грип")
        p2 = ChildPatient("Мария Петрова", 8, "Настинка")
        p3 = AdultPatient("Петър Георгиев", 45, "Преглед")

        patient_list = PatientList()
        patient_list.add_patient(p1)
        patient_list.add_patient(p2)
        patient_list.add_patient(p3)

        print("--- Iterating through all patients ---")
        for patient in patient_list:
            patient.display_info()

        print("\n--- Generating adult patients ---")
        for adult_patient in patient_list.adult_patients_generator():
            adult_patient.display_info()

    except ValueError as e:
        print(f"Validation Error: {e}")

