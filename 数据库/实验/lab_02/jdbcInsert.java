import java.sql.*;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;

public class jdbcInsert {
    public static void main(String args[]) {
        Connection c = null;
        Statement stmt = null;
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");

            c = DriverManager.getConnection(
                    "jdbc:mysql://localhost:3306/college?serverTimezone=Asia/Shanghai", "root", "121312QIUjiER+");
            System.out.println("Connect to database mysql successfully !");

            stmt = c.createStatement();
            String sql = "INSERT INTO employee VALUES "
                    + "(1, 'Gong', 48, '2075 Kongjiang Road', 20000.00),"
                    + "(2, 'Luan', 25, '3663 Zhongshan Road(N)', 15000.00),"
                    + "(3, 'Hu', 23, '3663 Zhongshan Road(N)', 15000.00),"
                    + "(4, 'Jin', 24, '3663 Zhongshan Road(N)', 15000.00),"
                    + "(5, 'Yi', 24, '3663 Zhongshan Road(N)', 15000.00);";
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
