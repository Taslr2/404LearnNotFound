import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.math.BigDecimal;
import java.sql.Statement;

public class jdbcPrepare {
    public static void main(String[] args) {
        Connection conn = null;
        PreparedStatement pst = null;
        Statement stmt = null;
        try {
            // 加载 MySQL 驱动
            Class.forName("com.mysql.cj.jdbc.Driver");

            // 连接到数据库
            conn = DriverManager.getConnection(
                    "jdbc:mysql://localhost:3306/college?serverTimezone=Asia/Shanghai",
                    "root",
                    "121312QIUjiER+");
            System.out.println("Connected to the database successfully!");

            //创建gpa关系
            stmt = conn.createStatement();
            String sql1 = "CREATE TABLE GPA(grade CHAR(2), grade_point DECIMAL(3,2))" ;

            stmt.executeUpdate(sql1);
            stmt.close();

            // 插入 SQL 语句
            String sql = "INSERT INTO GPA(grade, grade_point) VALUES (?, ?)";
            pst = conn.prepareStatement(sql);

            // 定义数据
            String[] strArray = new String[] {"A+","A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "D-", "F"};
            double[] doubleArray = new double[] {4.3, 4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.5, 1.3, 1.0, 0};

            // 遍历数据并添加到批处理
            for (int i = 0; i < strArray.length; i++) {
                pst.setString(1, strArray[i]);
                pst.setBigDecimal(2, BigDecimal.valueOf(doubleArray[i]));
                pst.addBatch();
            }

            // 执行批处理
            pst.executeBatch();
            System.out.println("Data inserted successfully!");

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                if (pst != null) pst.close();
                if (conn != null) conn.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}
