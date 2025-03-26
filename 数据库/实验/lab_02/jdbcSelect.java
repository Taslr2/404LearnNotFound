import java.sql.*;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;
import java.sql.ResultSet;

public class jdbcSelect {
    public static void main(String args[]) {
        Connection c = null;
        Statement stmt = null;
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");

            c = DriverManager.getConnection(
                    "jdbc:mysql://localhost:3306/college?serverTimezone=Asia/Shanghai", "root", "121312QIUjiER+");
            System.out.println("Connect to database mysql successfully !");

            stmt = c.createStatement();

            // 使用 executeQuery() 方法来处理 Select 语句
            String sql = "SELECT * FROM employee;";
            ResultSet rs = stmt.executeQuery(sql);

            // 遍历并打印查询结果
            while (rs.next()) {
                int id = rs.getInt("id");
                String name = rs.getString("name");
                int age = rs.getInt("age");
                String address = rs.getString("address");
                double salary = rs.getDouble("salary");

                System.out.println("ID: " + id + ", Name: " + name + ", Age: " + age +
                        ", Address: " + address + ", Salary: " + salary);
            }

            rs.close();
            stmt.close();
            c.close();
        } catch (Exception e) {
            System.err.println(e.getClass().getName() + ": " + e.getMessage());
            System.exit(0);
        }
        System.out.println("Select query executed successfully!");
    }
}
