import os
from datetime import datetime

class HospitalManagementSystem:
    def __init__(self):
        # File paths
        self.patients_file = "patients.txt"
        self.doctors_file = "doctors.txt"
        self.appointments_file = "appointments.txt"
        self.ambulances_file = "ambulances.txt"
        self.admin_password = "admin123"  # Admin password for authentication
        self.staff_file = "staff.txt"  
        self.rooms_file = "rooms.txt"
        self.medicine_file = "medicines.txt"

        # Load data from text files on startup
        self.patients = self.load_data(self.patients_file)
        self.doctors = self.load_data(self.doctors_file)
        self.appointments = self.load_data(self.appointments_file)
        self.ambulances = self.load_data(self.ambulances_file)
        self.staff = self.load_data(self.staff_file)
        self.rooms = self.load_data(self.rooms_file)
        self.medicines = self.load_data(self.medicine_file)

    def load_data(self, filename): 
        """ Load data from a file into a dictionary. """
        data = {}
        if os.path.exists(filename):
            with open(filename, "r") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        parts = line.split(",")
                        if filename == self.medicine_file:
                            if len(parts) >= 3:
                                data[parts[0]] = {"name": parts[1], "price": parts[2]}
                        else:
                            data[parts[0]] = parts[1:]
        return data

    def save_data(self, data, filename): 
        """ Save data from a dictionary to a file. """
        with open(filename, "w") as file:
            for key, value in data.items():
                if filename == self.medicine_file:
                    file.write(f"{key},{value['name']},{value['price']}\n")
                else:
                    file.write(f"{key},{','.join(value)}\n")

    def initialize_rooms(self):
        """Initialize 5 rooms of each type and save to rooms.txt."""
        rooms = {
            "R001": ["1", "General", "Floor 1", "Available"],
            "R002": ["1", "General", "Floor 1", "Available"],
            "R003": ["1", "General", "Floor 1", "Available"],
            "R004": ["1", "General", "Floor 1", "Available"],
            "R005": ["1", "General", "Floor 1", "Available"],
            "R006": ["2", "Semi-Private", "Floor 2", "Available"],
            "R007": ["2", "Semi-Private", "Floor 2", "Available"],
            "R008": ["2", "Semi-Private", "Floor 2", "Available"],
            "R009": ["2", "Semi-Private", "Floor 2", "Available"],
            "R010": ["2", "Semi-Private", "Floor 2", "Available"],
            "R011": ["3", "Private", "Floor 3", "Available"],
            "R012": ["3", "Private", "Floor 3", "Available"],
            "R013": ["3", "Private", "Floor 3", "Available"],
            "R014": ["3", "Private", "Floor 3", "Available"],
            "R015": ["3", "Private", "Floor 3", "Available"],
            "R016": ["4", "DELUX", "Floor 4", "Available"],
            "R017": ["4", "DELUX", "Floor 4", "Available"],
            "R018": ["4", "DELUX", "Floor 4", "Available"],
            "R019": ["4", "DELUX", "Floor 4", "Available"],
            "R020": ["4", "DELUX", "Floor 4", "Available"],
        }
        self.save_data(rooms, self.rooms_file)
        print("Rooms initialized and saved to rooms.txt successfully!")

    def allot_room(self):
        """Allot a room based on availability and patient preference."""
        print("\n--- Room Allotment ---")

        room_types = {
            "1": "General",
            "2": "Semi-Private",
            "3": "Private",
            "4": "ICU"
        }

        print("Available Room Types:")
        for key, value in room_types.items():
            print(f"{key}. {value}")

        choice = input("Select room type (1-4): ")
        if choice not in room_types:
            print("Invalid choice! Please select a valid room type.")
            return

        selected_type = room_types[choice]
        patient_id = input("Enter Patient ID: ")

        if patient_id not in self.patients:
            print("Patient ID not found! Please check and try again.")
            return

        # Check if the patient is already occupying a room
        for room_id, room_info in self.rooms.items():
            if len(room_info) > 4 and room_info[4] == patient_id:
                print(f"Patient {patient_id} is already occupying Room {room_id}. Cannot allot another room.")
                return

        # Find an available room of the selected type
        available_rooms = {k: v for k, v in self.rooms.items() if v[1] == selected_type and v[3] == "Available"}

        if not available_rooms:
            print(f"No {selected_type} rooms available at the moment.")
            return

        # Assign the first available room
        room_id, info = next(iter(available_rooms.items()))
        floor_no = info[0]

        # Mark room as occupied and add patient ID
        self.rooms[room_id][3] = "Occupied"
        self.rooms[room_id].append(patient_id)
        self.save_data(self.rooms, self.rooms_file)
        print(f"Room {room_id} ({selected_type}) on Floor {floor_no} allotted successfully to Patient ID {patient_id}.")

    def release_room(self):
        """Release an occupied room when a patient is discharged."""
        print("\n--- Release Room ---")
        room_id = input("Enter Room ID to release: ")

        if room_id in self.rooms and self.rooms[room_id][3] == "Occupied":
            self.rooms[room_id][3] = "Available"
            if len(self.rooms[room_id]) > 4:
                self.rooms[room_id].pop(-1)
            self.save_data(self.rooms, self.rooms_file)
            print(f"Room {room_id} is now available.")
        else:
            print("Invalid Room ID or the room is already available.")

    def view_room_status(self):
        """Display all rooms along with their current status."""
        print("\n--- Room Status ---")
        if not self.rooms:
            print("No rooms found!")
        else:
            for room_id, room_info in self.rooms.items():
                status = f"Room ID: {room_id}, Floor: {room_info[0]}, Type: {room_info[1]}, Status: {room_info[3]}"
                if len(room_info) > 4:
                    status += f", Occupied by Patient ID: {room_info[4]}"
                print(status)

    def view_room_status_a(self):
        """Display all rooms along with their current status (admin view)."""
        print("\n--- Room Status ---")
        if not self.rooms:
            print("No rooms found!")
        else:
            for room_id, room_info in self.rooms.items():
                status = f"Room ID: {room_id}, Floor: {room_info[0]}, Type: {room_info[1]}, Status: {room_info[3]}"
                if len(room_info) > 4:
                    status += f", Occupied by Patient ID: {room_info[4]}"
                print(status)

    def menu(self):
        while True:
            print("\n===== Hospital Management System =====")
            print("1. Login")
            print("2. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.login()
            elif choice == '2':
                print("Exiting the system...")
                break
            else:
                print("Invalid choice! Please try again.")

    def login(self):
        print("\n==== Login ====")
        user_type = input("Are you a user or admin? (Enter 'user' or 'admin'): ").strip().lower()

        if user_type == 'admin':
            self.admin_login()
        elif user_type == 'user':
            self.patient_login()
        else:
            print("Invalid choice! Please enter 'user' or 'admin'.")

    def admin_login(self):
        password = input("Enter admin password: ")
        if password == self.admin_password:
            print("Admin login successful!")
            self.admin_menu()
        else:
            print("Incorrect password! Access denied.")

    def admin_menu(self):
        while True:
            print("\n===== Admin Menu =====")
            print("1. Manage Patients")
            print("2. Manage Doctors")
            print("3. Schedule Appointment")
            print("4. View Appointments")
            print("5. Manage Staff")
            print("6. Manage ambulances")
            print("7. Manage medicine")
            print("8. View room status")
            print("9. Logout")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.manage_patients()
            elif choice == '2':
                self.manage_doctors()
            elif choice == '3':
                self.schedule_appointment()
            elif choice == '4':
                id = input("Enter patient id: ")
                self.view_patient_appointments(id)
            elif choice == '5':
                self.manage_staff()
            elif choice == '6':
                self.manage_ambulances()
            elif choice == '7':
                self.manage_medicine()
            elif choice == '8':
                self.view_room_status_a()
            elif choice == '9':
                print("Logging out...")
                break
            else:
                print("Invalid choice! Please try again.")

    def patient_login(self):
        st = input("Dial 108 to call ambulance? (Enter '108' to call or any key to continue): ")
        if st == '108':
            self.book_ambulance()
        else:
            print("(separate each symptom by ',')")
            dis = input("Enter your symptoms to check what kind of disease you might have: ")
            patient_id = input("Enter your patient ID: ")
            if patient_id in self.patients:
                print(f"Welcome, {self.patients[patient_id][0]}!")
                self.identify_disease(dis, patient_id)
            else:
                print("Patient ID not found! Please check and try again.")

    def buy_medicine(self, patient_id):
        """Allow patients to buy medicine using its ID."""
        print("\n--- Buy Medicine ---")
        if not self.medicines:
            print("No medicines available for purchase.")
            return
        
        print("\nAvailable Medicines:")
        for med_id, details in self.medicines.items():
            print(f"ID: {med_id}, Name: {details['name']}, Price: {details['price']}")
        
        med_id = input("Enter the Medicine ID you want to purchase: ")
        
        if med_id in self.medicines:
            medicine = self.medicines[med_id]
            print(f"\nYou have selected: {medicine['name']} (Price: {medicine['price']})")
            
            confirm = input("Confirm purchase? (yes/no): ").strip().lower()
            if confirm == "yes":
                purchase_record = {
                    "patient_id": patient_id,
                    "medicine_id": med_id,
                    "medicine_name": medicine["name"],
                    "price": medicine["price"],
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                print(f"Purchase successful! {medicine['name']} has been added to your records.")
                with open("medicine_purchases.txt", "a") as file:
                    file.write(f"{patient_id},{med_id},{medicine['name']},{medicine['price']},{purchase_record['date']}\n")
            else:
                print("Purchase cancelled.")
        else:
            print("Invalid Medicine ID. Please check and try again.")

    def identify_disease(self, report, patient_id=None):
        """Identify disease based on user-reported symptoms."""
        disease_symptoms = {
            "Flu": ["fever", "cough", "sore throat", "runny nose", "muscle aches"],
            "Cold": ["cough", "sore throat", "runny nose", "sneezing"],
            "Diabetes": ["increased thirst", "frequent urination", "extreme fatigue", "blurry vision"],
            "Hypertension": ["headache", "shortness of breath", "nosebleeds", "dizziness"],
            "Dengue": ["high fever", "severe headache", "joint pain", "skin rash", "fatigue"],
            "Asthma": ["wheezing", "shortness of breath", "chest tightness", "coughing"],
            "Food Poisoning": ["vomiting", "diarrhea", "stomach cramps", "nausea"],
            "Chickenpox": ["itchy rash", "red spots", "fever", "tiredness"],
            "Anemia": ["fatigue", "weakness", "pale skin", "shortness of breath"],
            "Migraine": ["severe headache", "nausea", "sensitivity to light", "blurred vision"]
        }
        
        identified_diseases = []
        report = report.lower()

        for disease, symptoms in disease_symptoms.items():
            if any(symptom in report for symptom in symptoms):
                identified_diseases.append(disease)
        
        if identified_diseases:
            print("Possible diseases based on your symptoms:", ", ".join(identified_diseases))
            print("Schedule the appointment with the doctor for treatment.")
            if patient_id:
                self.patient_menu(patient_id)
        else:
            print("No diseases identified based on the given symptoms.")
            print("Schedule the appointment with the doctor for further diagnosis.")
            if patient_id:
                self.patient_menu(patient_id)

    def manage_patients(self):
        while True:
            print("\n==== Manage Patients ====")
            print("1. Add Patient")
            print("2. View Patients")
            print("3. Update Patient")
            print("4. Delete Patient")
            print("5. Back to Admin Menu")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.add_patient()
            elif choice == '2':
                self.view_patients()
            elif choice == '3':
                self.update_patient()
            elif choice == '4':
                self.delete_patient()
            elif choice == '5':
                break
            else:
                print("Invalid choice! Please try again.")

    def patient_menu(self, patient_id):
        while True:
            print("\n===== Patient Menu =====")
            print("1. View Your Information")
            print("2. View Appointments")
            print("3. Schedule Appointment")
            print("4. Buy Medicine")
            print("5. Book a Room")
            print("6. View room status")
            print("7. Release room")
            print("8. Logout")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.view_patient_info(patient_id)
            elif choice == '2':
                self.view_patient_appointments(patient_id)
            elif choice == '3':
                self.schedule_appointment(patient_id)
            elif choice == '4':
                self.buy_medicine(patient_id)
            elif choice == '5':
                self.allot_room()
            elif choice == '6':
                self.view_room_status()
            elif choice == '7':
                self.release_room()
            elif choice == '8':
                print("Logging out...")
                break
            else:
                print("Invalid choice! Please try again.")

    def add_patient(self):
        print("\n--- Add New Patient ---")
        patient_id = input("Enter Patient ID: ")
        if patient_id in self.patients:
            print("Patient ID already exists!")
            return
            
        name = input("Enter Patient Name: ")
        while True:
            age = input("Enter Patient Age: ")
            if age.isdigit() and 0 < int(age) < 100:
                break
            print("Invalid age! Age must be a number between 1 and 99.")
        disease = input("Enter Patient Disease: ")
        self.patients[patient_id] = [name, age, disease]
        self.save_data(self.patients, self.patients_file)
        print("Patient added successfully!")

    def view_patients(self):
        if not self.patients:
            print("No patients found!")
        else:
            for patient_id, patient_info in self.patients.items():
                print(f"ID: {patient_id}, Name: {patient_info[0]}, Age: {patient_info[1]}, Disease: {patient_info[2]}")

    def update_patient(self):
        patient_id = input("Enter Patient ID to update: ")
        if patient_id in self.patients:
            name = input("Enter new Patient Name: ")
            while True:
                age = input("Enter Patient Age: ")
                if age.isdigit() and 0 < int(age) < 100:
                    break
                print("Invalid age! Age must be a number between 1 and 99.")
            disease = input("Enter new Patient Disease: ")
            self.patients[patient_id] = [name, age, disease]
            self.save_data(self.patients, self.patients_file)
            print("Patient updated successfully!")
        else:
            print("Patient ID not found!")

    def delete_patient(self):
        patient_id = input("Enter Patient ID to delete: ")
        if patient_id in self.patients:
            del self.patients[patient_id]
            self.save_data(self.patients, self.patients_file)
            print("Patient deleted successfully!")
        else:
            print("Patient ID not found!")

    def manage_medicine(self):
        while True:
            print("\n==== Manage Medicine ====")
            print("1. Add Medicine")
            print("2. Update Medicine")
            print("3. Delete Medicine")
            print("4. Display Medicines")
            print("5. Back to Admin Menu")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.add_medicine()
            elif choice == '2':
                self.update_medicine()
            elif choice == '3':
                self.delete_medicine()
            elif choice == '4':
                self.display_medicines()
            elif choice == '5':
                break
            else:
                print("Invalid choice! Please try again.")

    def add_medicine(self):
        print("\n--- Add New Medicine ---")
        med_id = input("Enter Medicine ID: ")
        if med_id in self.medicines:
            print("Medicine ID already exists!")
            return
            
        name = input("Enter Medicine Name: ")
        while True:
            price = input("Enter Medicine Price: ")
            try:
                price = float(price)
                if price > 0:
                    break
                print("Price must be a positive number!")
            except ValueError:
                print("Invalid price! Please enter a valid number.")
                
        self.medicines[med_id] = {"name": name, "price": str(price)}
        self.save_data(self.medicines, self.medicine_file)
        print("Medicine added successfully!")

    def update_medicine(self):
        med_id = input("Enter Medicine ID to update: ")
        if med_id in self.medicines:
            name = input(f"Current name: {self.medicines[med_id]['name']}\nEnter new name (press enter to keep current): ")
            if name:
                self.medicines[med_id]['name'] = name
                
            while True:
                price = input(f"Current price: {self.medicines[med_id]['price']}\nEnter new price (press enter to keep current): ")
                if not price:
                    break
                try:
                    price = float(price)
                    if price > 0:
                        self.medicines[med_id]['price'] = str(price)
                        break
                    print("Price must be a positive number!")
                except ValueError:
                    print("Invalid price! Please enter a valid number.")
                    
            self.save_data(self.medicines, self.medicine_file)
            print("Medicine updated successfully!")
        else:
            print("Medicine ID not found!")

    def delete_medicine(self):
        med_id = input("Enter Medicine ID to delete: ")
        if med_id in self.medicines:
            del self.medicines[med_id]
            self.save_data(self.medicines, self.medicine_file)
            print("Medicine deleted successfully!")
        else:
            print("Medicine ID not found!")

    def display_medicines(self):
        if not self.medicines:
            print("No medicines available.")
        else:
            print("\nMedicine List:")
            for med_id, details in self.medicines.items():
                print(f"ID: {med_id}, Name: {details['name']}, Price: {details['price']}")

    def manage_doctors(self):
        while True:
            print("\n==== Manage Doctors ====")
            print("1. Add Doctor")
            print("2. View Doctors")
            print("3. Update Doctor")
            print("4. Delete Doctor")
            print("5. Back to Admin Menu")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.add_doctor()
            elif choice == '2':
                self.view_doctors()
            elif choice == '3':
                self.update_doctor()
            elif choice == '4':
                self.delete_doctor()
            elif choice == '5':
                break
            else:
                print("Invalid choice! Please try again.")

    def add_doctor(self):
        print("\n--- Add New Doctor ---")
        while True:
            doctor_id = input("Enter Doctor ID: ")
            if doctor_id not in self.doctors:
                break
            print("This ID already exists. Please use a unique ID.")
            
        name = input("Enter Doctor Name: ")
        specialty = input("Enter Doctor Specialty: ")
        while True:
            contact = input("Enter Doctor Contact: ")
            if len(contact) == 10 and contact[0] in "9876":
                break
            print("Invalid phone number! It should be 10 digits and start with 9, 8, 7, or 6.")
            
        self.doctors[doctor_id] = [name, specialty, contact]
        self.save_data(self.doctors, self.doctors_file)
        print("Doctor added successfully!")

    def view_doctors(self):
        if not self.doctors:
            print("No doctors found!")
        else:
            for doctor_id, doctor_info in self.doctors.items():
                print(f"ID: {doctor_id}, Name: {doctor_info[0]}, Specialty: {doctor_info[1]}, Contact: {doctor_info[2]}")

    def update_doctor(self):
        doctor_id = input("Enter Doctor ID to update: ")
        if doctor_id in self.doctors:
            name = input("Enter new Doctor Name: ")
            specialty = input("Enter new Doctor Specialty: ")
            while True:
                contact = input("Enter new Doctor Contact: ")
                if len(contact) == 10 and contact[0] in "9876":
                    break
                print("Invalid phone number! It should be 10 digits and start with 9, 8, 7, or 6.")
                
            self.doctors[doctor_id] = [name, specialty, contact]
            self.save_data(self.doctors, self.doctors_file)
            print("Doctor updated successfully!")
        else:
            print("Doctor ID not found!")

    def delete_doctor(self):
        doctor_id = input("Enter Doctor ID to delete: ")
        if doctor_id in self.doctors:
            del self.doctors[doctor_id]
            self.save_data(self.doctors, self.doctors_file)
            print("Doctor deleted successfully!")
        else:
            print("Doctor ID not found!")

    def validate_date(self, date_str):
        try:
            appointment_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            today_date = datetime.today().date()
            if appointment_date >= today_date:
                return True
            else:
                print("Invalid date! You cannot schedule an appointment in the past.")
                return False
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return False

    def is_valid_24_hour_time(self, time_str):
        parts = time_str.split(":")
        if len(parts) != 2:
            return False
        hours, minutes = parts
        if not (hours.isdigit() and minutes.isdigit()):
            return False
        hours, minutes = int(hours), int(minutes)
        return 0 <= hours < 24 and 0 <= minutes < 60

    def is_appointment_conflict(self, doctor_id, date, time):
        for appointment_id, appointment_info in self.appointments.items():
            if appointment_info[1] == doctor_id and appointment_info[2] == date and appointment_info[3] == time:
                return True
        return False

    def schedule_appointment(self, patient_id=None):
        if patient_id is None:
            patient_id = input("Enter Patient ID: ")
        if patient_id not in self.patients:
            print("Patient not found!")
            return

        doctor_id = input("Enter Doctor ID: ")
        if doctor_id not in self.doctors:
            print("Doctor not found!")
            return

        while True:
            date = input("Enter Appointment Date (YYYY-MM-DD): ")
            if self.validate_date(date):
                break

        while True:
            time = input("Enter Appointment Time (HH:MM): ")
            if self.is_valid_24_hour_time(time):
                if self.is_appointment_conflict(doctor_id, date, time):
                    print(f"Conflict! Doctor is already booked for {time} on {date}. Please choose another time.")
                else:
                    break
            else:
                print("Invalid time! Please enter a valid 24-hour format time (HH:MM).")

        appointment_id = f"{patient_id}{doctor_id}{date}_{time}"
        self.appointments[appointment_id] = [patient_id, doctor_id, date, time]
        self.save_data(self.appointments, self.appointments_file)
        print("Appointment scheduled successfully!")

    def view_patient_info(self, patient_id):
        if patient_id in self.patients:
            patient = self.patients[patient_id]
            print(f"ID: {patient_id}, Name: {patient[0]}, Age: {patient[1]}, Disease: {patient[2]}")
        else:
            print("Patient ID not found!")

    def view_patient_appointments(self, patient_id):
        appointments_found = False
        for appointment_id, appointment_info in self.appointments.items():
            if appointment_info[0] == patient_id:
                doctor = self.doctors[appointment_info[1]][0]
                date = appointment_info[2]
                time = appointment_info[3]
                print(f"Appointment with Dr. {doctor} on {date} at {time}")
                appointments_found = True
        if not appointments_found:
            print("No appointments found.")

    def manage_staff(self):
        while True:
            print("\n==== Manage Staff ====")
            print("1. Add Staff Member")
            print("2. View Staff Members")
            print("3. Update Staff Member")
            print("4. Delete Staff Member")
            print("5. Back to Admin Menu")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.add_staff()
            elif choice == '2':
                self.view_staff()
            elif choice == '3':
                self.update_staff()
            elif choice == '4':
                self.delete_staff()
            elif choice == '5':
                break
            else:
                print("Invalid choice! Please try again.")

    def add_staff(self):
        print("\n--- Add New Staff Member ---")
        staff_id = input("Enter Staff ID: ")
        if staff_id in self.staff:
            print("This ID already exists. Please use a unique ID.")
            return

        name = input("Enter Staff Name: ")
        role = input("Enter Staff Role (e.g., Nurse, Technician, Receptionist, sweeper, cleaner): ")
        
        while True:
            contact = input("Enter Staff Contact Number: ")
            if len(contact) == 10 and contact[0] in "9876":
                break
            print("Invalid phone number! It should be 10 digits and start with 9, 8, 7, or 6.")

        self.staff[staff_id] = [name, role, contact]
        self.save_data(self.staff, self.staff_file)
        print("Staff member added successfully!")

    def view_staff(self):
        if not self.staff:
            print("No staff members found!")
        else:
            print("\n--- Staff Members ---")
            for staff_id, staff_info in self.staff.items():
                print(f"ID: {staff_id}, Name: {staff_info[0]}, Role: {staff_info[1]}, Contact: {staff_info[2]}")

    def update_staff(self):
        staff_id = input("Enter Staff ID to update: ")
        if staff_id in self.staff:
            name = input("Enter new Staff Name: ")
            role = input("Enter new Staff Role: ")
            
            while True:
                contact = input("Enter new Contact Number: ")
                if len(contact) == 10 and contact[0] in "9876":
                    break
                print("Invalid phone number! It should be 10 digits and start with 9, 8, 7, or 6.")
            
            self.staff[staff_id] = [name, role, contact]
            self.save_data(self.staff, self.staff_file)
            print("Staff member updated successfully!")
        else:
            print("Staff ID not found!")

    def delete_staff(self):
        staff_id = input("Enter Staff ID to delete: ")
        if staff_id in self.staff:
            del self.staff[staff_id]
            self.save_data(self.staff, self.staff_file)
            print("Staff member deleted successfully!")
        else:
            print("Staff ID not found!")

    def manage_ambulances(self):
        while True:
            print("\n==== Manage Ambulances ====")
            print("1. Add Ambulance")
            print("2. View Ambulances")
            print("3. Update Ambulance")
            print("4. Delete Ambulance")
            print("5. Back to Admin Menu")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.add_ambulances()
            elif choice == '2':
                self.view_ambulances()
            elif choice == '3':
                self.update_ambulances()
            elif choice == '4':
                self.delete_ambulances()
            elif choice == '5':
                break
            else:
                print("Invalid choice! Please try again.")

    def add_ambulances(self):
        print("\n--- Add New Ambulance ---")
        ambulance_id = input("Enter Ambulance ID: ")
        if ambulance_id in self.ambulances:
            print("Ambulance ID already exists!")
            return
            
        driver_name = input("Enter Driver Name: ")
        status = "Available"
        self.ambulances[ambulance_id] = [driver_name, status]
        self.save_data(self.ambulances, self.ambulances_file)
        print("Ambulance added successfully!")

    def view_ambulances(self):
        if not self.ambulances:
            print("No ambulances found!")
        else:
            for ambulance_id, info in self.ambulances.items():
                print(f"ID: {ambulance_id}, Driver: {info[0]}, Status: {info[1]}")

    def update_ambulances(self):
        ambulance_id = input("Enter Ambulance ID to update: ")
        if ambulance_id in self.ambulances:
            driver_name = input("Enter new Driver Name: ")
            status = input("Enter new Status (Available/Booked): ").capitalize()
            if status not in ["Available", "Booked"]:
                print("Invalid status! Setting to 'Available'.")
                status = "Available"
            self.ambulances[ambulance_id] = [driver_name, status]
            self.save_data(self.ambulances, self.ambulances_file)
            print("Ambulance updated successfully!")
        else:
            print("Ambulance ID not found!")

    def delete_ambulances(self):
        ambulance_id = input("Enter Ambulance ID to delete: ")
        if ambulance_id in self.ambulances:
            del self.ambulances[ambulance_id]
            self.save_data(self.ambulances, self.ambulances_file)
            print("Ambulance deleted successfully!")
        else:
            print("Ambulance ID not found!")

    def book_ambulance(self):
        print("\n--- Book an Ambulance ---")
        available_ambulances = {k: v for k, v in self.ambulances.items() if v[1] == "Available"}

        if not available_ambulances:
            print("No ambulances are available at the moment.")
            return

        ambulance_id, info = next(iter(available_ambulances.items()))
        driver_name = info[0]

        self.ambulances[ambulance_id][1] = "Booked"
        self.save_data(self.ambulances, self.ambulances_file)

        print(f"Ambulance ID: {ambulance_id} (Driver: {driver_name}) has been booked successfully!")

# Main program execution
if __name__ == "__main__":
    hospital_system = HospitalManagementSystem()
    hospital_system.menu()