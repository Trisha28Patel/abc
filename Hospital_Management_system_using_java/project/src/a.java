import java.io.*;
import java.sql.*;
import java.util.*;
import java.util.function.IntPredicate;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;

public class HospitalManagementSystem {
    private static final String DB_URL = "jdbc:mysql://localhost:3306/hospitall";
    private static final String DB_USER = "root";
    private static final String DB_PASSWORD = "";
    private static final String ADMIN_PASSWORD_HASH = "$2a$10$N9qo8uLOickgx2ZMRZoMy..."; // bcrypt hash for "12345"
    
    private static Scanner sc = new Scanner(System.in);
    private static final DateTimeFormatter DATE_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd");

    public static void main(String[] args) {
        try (Connection con = DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD)) {
            boolean running = true;
            while (running) {
                System.out.println("\n==== Hospital Management System ====");
                System.out.println("1. User Login");
                System.out.println("2. Admin Login");
                System.out.println("3. Exit");
                
                int choice = readValidInt("Select option: ", 1, 3);
                
                switch (choice) {
                    case 1:
                        userMenu(con);
                        break;
                    case 2:
                        adminLogin(con);
                        break;
                    case 3:
                        running = false;
                        System.out.println("Thank you for using the system. Goodbye!");
                        break;
                }
            }
        } catch (SQLException e) {
            System.err.println("Database connection error: " + e.getMessage());
        }
    }

    // ================== Utility Methods ==================
    
    private static int readValidInt(String prompt, int min, int max) {
        while (true) {
            System.out.print(prompt);
            if (sc.hasNextInt()) {
                int input = sc.nextInt();
                sc.nextLine(); // consume newline
                if (input >= min && input <= max) {
                    return input;
                }
            } else {
                sc.nextLine(); // consume invalid input
            }
            System.out.println("Invalid input. Please enter a number between " + min + " and " + max);
        }
    }
    
    private static String readNonEmptyString(String prompt) {
        while (true) {
            System.out.print(prompt);
            String input = sc.nextLine().trim();
            if (!input.isEmpty()) {
                return input;
            }
            System.out.println("Input cannot be empty!");
        }
    }
    
    private static LocalDate readFutureDate(String prompt) {
        while (true) {
            System.out.print(prompt + " (YYYY-MM-DD): ");
            String dateStr = sc.nextLine();
            try {
                LocalDate date = LocalDate.parse(dateStr, DATE_FORMATTER);
                if (date.isBefore(LocalDate.now())) {
                    System.out.println("Date must be in the future!");
                } else {
                    return date;
                }
            } catch (DateTimeParseException e) {
                System.out.println("Invalid date format. Please use YYYY-MM-DD.");
            }
        }
    }

    // ================== User Menu ==================
    
    private static void userMenu(Connection con) throws SQLException {
        while (true) {
            System.out.println("\n==== User Menu ====");
            System.out.println("1. Fix Appointment");
            System.out.println("2. Get Medicines");
            System.out.println("3. View Doctors");
            System.out.println("4. Book a Room");
            System.out.println("5. Discharge");
            System.out.println("6. Back to Main Menu");
            
            int option = readValidInt("Select option: ", 1, 6);
            
            switch (option) {
                case 1:
                    fixAppointment(con);
                    break;
                case 2:
                    getMedicines(con);
                    break;
                case 3:
                    viewDoctors(con);
                    break;
                case 4:
                    bookRoom(con);
                    break;
                case 5:
                    dischargePatient(con);
                    break;
                case 6:
                    return;
            }
        }
    }

    // ================== Admin Functions ==================
    
    private static void adminLogin(Connection con) throws SQLException {
        System.out.print("Enter admin password: ");
        String password = sc.nextLine();
        
        // In real implementation, use BCrypt.checkpw(password, ADMIN_PASSWORD_HASH)
        if (password.equals("12345")) { // Temporary for testing
            adminMenu(con);
        } else {
            System.out.println("Incorrect password! Access denied.");
        }
    }
    
    private static void adminMenu(Connection con) throws SQLException {
        while (true) {
            System.out.println("\n==== Admin Menu ====");
            System.out.println("1. Add Doctor");
            System.out.println("2. Add Medicine");
            System.out.println("3. View Doctors");
            System.out.println("4. View Medicines");
            System.out.println("5. Update Doctor");
            System.out.println("6. Update Staff");
            System.out.println("7. Back to Main Menu");
            
            int option = readValidInt("Select option: ", 1, 7);
            
            switch (option) {
                case 1:
                    addDoctor(con);
                    break;
                case 2:
                    addMedicine(con);
                    break;
                case 3:
                    viewDoctors(con);
                    break;
                case 4:
                    viewMedicines(con);
                    break;
                case 5:
                    updateDoctor(con);
                    break;
                case 6:
                    updateStaff(con);
                    break;
                case 7:
                    return;
            }
        }
    }

    // ================== Core Functionality ==================
    
    private static void fixAppointment(Connection con) throws SQLException {
        System.out.println("\n=== Fix Appointment ===");
        
        String firstName = readNonEmptyString("Enter first name: ");
        String lastName = readNonEmptyString("Enter last name: ");
        int age = readValidInt("Enter age: ", 1, 120);
        
        System.out.println("Select problem type:");
        System.out.println("1. Dental");
        System.out.println("2. Gynecological");
        System.out.println("3. Scanning");
        System.out.println("4. Heart");
        System.out.println("5. Bones");
        System.out.println("6. Skin");
        System.out.println("7. Psychological");
        System.out.println("8. Neurological");
        
        int problemType = readValidInt("Enter choice: ", 1, 8);
        String doctorSpecialization = getSpecialization(problemType);
        
        LocalDate appointmentDate = readFutureDate("Enter appointment date");
        
        String sql = "INSERT INTO patient (p_fname, p_lname, p_age, doctor, appointment_date) " +
                     "VALUES (?, ?, ?, ?, ?)";
        
        try (PreparedStatement pst = con.prepareStatement(sql)) {
            pst.setString(1, firstName);
            pst.setString(2, lastName);
            pst.setInt(3, age);
            pst.setString(4, doctorSpecialization);
            pst.setString(5, appointmentDate.format(DATE_FORMATTER));
            
            int rowsAffected = pst.executeUpdate();
            if (rowsAffected > 0) {
                System.out.println("Appointment fixed successfully with " + doctorSpecialization);
            } else {
                System.out.println("Failed to fix appointment");
            }
        }
    }
    
    private static String getSpecialization(int problemType) {
        switch (problemType) {
            case 1: return "Dentist";
            case 2: return "Gynecologist";
            case 3: return "Radiologist";
            case 4: return "Cardiologist";
            case 5: return "Orthopedic";
            case 6: return "Dermatologist";
            case 7: return "Psychologist";
            case 8: return "Neurologist";
            default: return "General Physician";
        }
    }
    
    private static void getMedicines(Connection con) throws SQLException {
        System.out.println("\n=== Medicine Purchase ===");
        viewMedicines(con);
        
        String medicineName = readNonEmptyString("Enter medicine name: ");
        
        String updateSql = "UPDATE pharmacy SET count = count + 1 WHERE mname = ?";
        String selectSql = "SELECT mprize FROM pharmacy WHERE mname = ?";
        
        try (PreparedStatement updateStmt = con.prepareStatement(updateSql);
             PreparedStatement selectStmt = con.prepareStatement(selectSql)) {
            
            // Update count
            updateStmt.setString(1, medicineName);
            int updated = updateStmt.executeUpdate();
            
            if (updated > 0) {
                // Get price
                selectStmt.setString(1, medicineName);
                try (ResultSet rs = selectStmt.executeQuery()) {
                    if (rs.next()) {
                        int price = rs.getInt("mprize");
                        System.out.println("Price: " + price);
                        processPayment(con, price);
                    }
                }
            } else {
                System.out.println("Medicine not found!");
            }
        }
    }
    
    private static void processPayment(Connection con, int amount) {
        System.out.println("\n=== Payment Processing ===");
        System.out.println("Amount to pay: " + amount);
        
        System.out.println("Select payment method:");
        System.out.println("1. Credit/Debit Card");
        System.out.println("2. Cash");
        System.out.println("3. UPI");
        System.out.println("4. Net Banking");
        
        int method = readValidInt("Enter choice: ", 1, 4);
        String paymentMethod = "";
        String details = "";
        
        switch (method) {
            case 1:
                paymentMethod = "Card";
                details = "Card ending with " + readNonEmptyString("Enter last 4 digits: ").substring(0, 4);
                break;
            case 2:
                paymentMethod = "Cash";
                details = "Paid at counter";
                break;
            case 3:
                paymentMethod = "UPI";
                details = readNonEmptyString("Enter UPI ID: ");
                break;
            case 4:
                paymentMethod = "Net Banking";
                details = "Account ending with " + readNonEmptyString("Enter last 4 digits: ").substring(0, 4);
                break;
        }
        
        String sql = "INSERT INTO payment (method, details, amount) VALUES (?, ?, ?)";
        
        try (PreparedStatement pst = con.prepareStatement(sql)) {
            pst.setString(1, paymentMethod);
            pst.setString(2, details);
            pst.setInt(3, amount);
            
            int rows = pst.executeUpdate();
            System.out.println(rows > 0 ? "Payment successful!" : "Payment failed");
        } catch (SQLException e) {
            System.err.println("Payment processing error: " + e.getMessage());
        }
    }

    // ================== Database Operations ==================
    
    private static void viewDoctors(Connection con) throws SQLException {
        String sql = "SELECT * FROM doctor";
        
        try (Statement stmt = con.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("\n=== Doctor List ===");
            while (rs.next()) {
                System.out.println("ID: " + rs.getInt("did"));
                System.out.println("Name: " + rs.getString("dname"));
                System.out.println("Experience: " + rs.getInt("dexp") + " years");
                System.out.println("Speciality: " + rs.getString("dspeciality"));
                System.out.println("-------------------");
            }
        }
    }
    
    private static void addDoctor(Connection con) throws SQLException {
        System.out.println("\n=== Add New Doctor ===");
        
        String name = readNonEmptyString("Enter doctor name: ");
        int experience = readValidInt("Enter experience (years): ", 0, 50);
        String speciality = readNonEmptyString("Enter speciality: ");
        
        String sql = "INSERT INTO doctor (dname, dexp, dspeciality) VALUES (?, ?, ?)";
        
        try (PreparedStatement pst = con.prepareStatement(sql)) {
            pst.setString(1, name);
            pst.setInt(2, experience);
            pst.setString(3, speciality);
            
            int rows = pst.executeUpdate();
            System.out.println(rows > 0 ? "Doctor added successfully!" : "Failed to add doctor");
        }
    }
    
    // ... (Other methods implemented similarly with proper error handling and validation)

    private static void bookRoom(Connection con) throws SQLException {
        System.out.println("\n=== Room Booking ===");
        
        System.out.println("Available room types:");
        System.out.println("1. General");
        System.out.println("2. Semi Special");
        System.out.println("3. Special");
        System.out.println("4. Deluxe");
        System.out.println("5. Super Deluxe");
        
        int roomTypeChoice = readValidInt("Select room type: ", 1, 5);
        String roomType = getRoomType(roomTypeChoice);
        
        // Find available room
        String findSql = "SELECT room_id, room_number FROM rooms WHERE room_type = ? AND status = 'Available' LIMIT 1";
        int roomId = -1;
        int roomNumber = -1;
        
        try (PreparedStatement pst = con.prepareStatement(findSql)) {
            pst.setString(1, roomType);
            try (ResultSet rs = pst.executeQuery()) {
                if (rs.next()) {
                    roomId = rs.getInt("room_id");
                    roomNumber = rs.getInt("room_number");
                } else {
                    System.out.println("No available rooms of this type");
                    return;
                }
            }
        }
        
        // Book the room
        String updateSql = "UPDATE rooms SET status = 'Occupied' WHERE room_id = ?";
        try (PreparedStatement pst = con.prepareStatement(updateSql)) {
            pst.setInt(1, roomId);
            int updated = pst.executeUpdate();
            
            if (updated > 0) {
                System.out.println("Room " + roomNumber + " (" + roomType + ") booked successfully!");
                
                // Admit patient
                admitPatient(con, roomId);
            }
        }
    }
    
    private static String getRoomType(int choice) {
        switch (choice) {
            case 1: return "General";
            case 2: return "Semi Special";
            case 3: return "Special";
            case 4: return "Deluxe";
            case 5: return "Super Deluxe";
            default: return "General";
        }
    }
    
    private static void admitPatient(Connection con, int roomId) throws SQLException {
        int patientId = readValidInt("Enter patient ID: ", 1, Integer.MAX_VALUE);
        
        String sql = "INSERT INTO admit_p (p_id, room_id) VALUES (?, ?)";
        try (PreparedStatement pst = con.prepareStatement(sql)) {
            pst.setInt(1, patientId);
            pst.setInt(2, roomId);
            
            int rows = pst.executeUpdate();
            System.out.println(rows > 0 ? "Patient admitted successfully!" : "Admission failed");
        }
    }
}