import java.sql.*;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;

public class jdbcCreate {
    public static void main(String args[]) {
        Connection c = null;
        Statement stmt = null;
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");

            c = DriverManager.getConnection(
                    "jdbc:mysql://localhost:3306/college?serverTimezone=Asia/Shanghai", "root", "121312QIUjiER+");
            System.out.println("Connect to database mysql successfully !");

            stmt = c.createStatement();
            String sql = "CREATE TABLE employee (id INT," +
                    " name VARCHAR(20) NOT NULL, " +
                    " age INT NOT NULL, " +
                    " address VARCHAR(50), " +
                    " salary REAL, " +
                    "PRIMARY KEY (id))";
            stmt.executeUpdate(sql);
            stmt.close();
            c.close();
        } catch (Exception e) {
            System.err.println(e.getClass().getName() + ": " + e.getMessage());
            System.exit(0);
        }
        System.out.println("Create table company successfully !");
    }
}
