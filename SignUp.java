import java.util.*;
import java.io.*;

public class SignUp {
    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.println("=== SIGN UP ===");
        System.out.println("1. Student");
        System.out.println("2. Professor");
        System.out.println("3. Admin");
        System.out.print("Choose: ");

        int choice = sc.nextInt();
        sc.nextLine();

        try {
            File directory = new File("Database");
            if (!directory.exists()) {
                directory.mkdir();
            }

            FileWriter fw = new FileWriter("Database/Accounts.txt", true);

            switch (choice) {
                case 1:
                    studentSignUp(sc, fw);
                    break;
                case 2:
                    professorSignUp(sc, fw);
                    break;
                case 3:
                    adminSignUp(sc, fw);
                    break;
                default:
                    System.out.println("Invalid option.");
            }

            fw.close();
        } catch (Exception e) {
            System.out.println("Error writing to file.");
        }
    }


    private static void studentSignUp(Scanner sc, FileWriter fw) throws Exception {
        System.out.print("Enter full name: ");
        String name = sc.nextLine();

        System.out.print("Enter classification: ");
        String classification = sc.nextLine();

        System.out.print("Enter major: ");
        String major = sc.nextLine();

        String id = generateID("900");

        fw.write("STUDENT," + id + "," + name + "," + classification + "," + major + ",false\n");

        System.out.println("\nAccount created successfully!");
        System.out.println("Name: " + name);
        System.out.println("ID: " + id);
    }


    private static void professorSignUp(Scanner sc, FileWriter fw) throws Exception {
        String pin = loadPin("professor");

        int attempts = 0;
        while (attempts < 3) {

            System.out.print("Enter professor PIN: ");
            String entered = sc.nextLine();

            if (entered.equals(pin)) {
                System.out.print("Enter full name: ");
                String name = sc.nextLine();
                String id = generateID("700");

                fw.write("PROFESSOR," + id + "," + name + "\n");

                System.out.println("\nAccount created successfully!");
                System.out.println("Name: " + name);
                System.out.println("ID: " + id);
                return;
            }
            attempts++;
        }

        System.out.println("Too many attempts. Closing Java...");
        System.exit(0);
    }



    private static void adminSignUp(Scanner sc, FileWriter fw) throws Exception {
        String pin = loadPin("admin");

        int attempts = 0;
        while (attempts < 3) {

            System.out.print("Enter admin PIN: ");
            String entered = sc.nextLine();

            if (entered.equals(pin)) {
                System.out.print("Enter name: ");
                String name = sc.nextLine();
                String id = generateID("800");

                fw.write("ADMIN," + id + "," + name + "\n");

                System.out.println("\nAccount created successfully!");
                System.out.println("Name: " + name);
                System.out.println("ID: " + id);
                return;
            }
            attempts++;
        }

        System.out.println("Too many attempts. Closing Java...");
        System.exit(0);
    }


    private static String loadPin(String type) throws Exception {
        BufferedReader br = new BufferedReader(new FileReader("Database/Security_pins.txt"));
        String line;
        while ((line = br.readLine()) != null) {
            if (line.startsWith(type + ":")) {
                return line.split(":")[1].trim();
            }
        }
        return "";
    }

    private static String generateID(String prefix) {
        Random rand = new Random();
        return prefix + (100000 + rand.nextInt(900000));
    }
}
