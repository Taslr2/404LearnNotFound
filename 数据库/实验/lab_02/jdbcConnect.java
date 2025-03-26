import java.sql.Connection;
import java.sql.DriverManager;
public class jdbcConnect {
    public static void main(String args[]){
        Connection c=null; try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            c = DriverManager.getConnection("jdbc:mysql://localhost:3306/college?serverTimezone=Asia/Shanghai", "root", "121312QIUjiER+");
        }
        catch(Exception e) {
            e.printStackTrace();
            System.err.println(e.getClass().getName() + ":" + e.getMessage());
            System.exit(0);
        }
                System.out.println("Connect to database mysql successfully !"
                );
            }
        }