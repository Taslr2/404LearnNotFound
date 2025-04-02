import java.sql.*;
import java.util.Scanner;

public class Homework {
    public static void main(String args[]) {
        Connection c = null;
        Statement stmt = null;
        Scanner in = new Scanner(System.in);
        boolean connectionSuccess = false;

        // 2.1 连接数据库，失败允许重试
        while (!connectionSuccess) {
            try {
                // Prompt for database credentials
                System.out.println("请输入数据库用户名:");
                String username = in.nextLine();

                System.out.println("请输入数据库密码:");
                String password = in.nextLine();

                Class.forName("com.mysql.cj.jdbc.Driver");
                c = DriverManager.getConnection(
                        "jdbc:mysql://localhost:3306/college?serverTimezone=Asia/Shanghai",
                        username,
                        password
                );

                System.out.println("数据库连接成功！");
                connectionSuccess = true;

            } catch (Exception e) {
                System.out.println("连接失败：" + e.getMessage());
                System.out.println("是否重试？(1:是/0:否)");
                if (in.nextInt() != 1) {
                    System.out.println("程序退出");
                    return ;
                }
                in.nextLine(); // 清除输入缓冲
            }
        }

        try {
            stmt = c.createStatement();

// 2.2 查询包含指定字符串的学生信息
            boolean hasResult = false;
            while (!hasResult) {
                try {
                    System.out.println("请输入要查询的名字（将返回名字中包含该字符串的所有学生信息）：");
                    String searchString = in.nextLine();
                    if (searchString.isEmpty()) {
                        searchString = in.nextLine(); // 处理可能的空行
                    }

                    // 使用 LIKE 操作符进行模糊查询
                    String sql = "SELECT id, name, dept_name, tot_cred FROM student WHERE name LIKE ?";
                    PreparedStatement pstmt = c.prepareStatement(sql);
                    pstmt.setString(1, "%" + searchString + "%");  // 使用%实现包含查询

                    ResultSet rs = pstmt.executeQuery();
                    if (!rs.isBeforeFirst()) {
                        System.out.println("未找到包含 '" + searchString + "' 的学生姓名，是否重新输入？(1:是/0:否)");
                        if (in.nextInt() != 1) {
                            return;
                        }
                        in.nextLine();
                        continue;
                    }

                    System.out.println("\n查询结果：");
                    while (rs.next()) {
                        hasResult = true;
                        String studentId = rs.getString("ID");
                        String studentName = rs.getString("name");
                        String studentDept = rs.getString("dept_name");
                        int studentCred = rs.getInt("tot_cred");

                        System.out.println("ID: " + studentId +
                                ", Name: " + studentName +
                                ", Department: " + studentDept +
                                ", Total Credits: " + studentCred);
                    }
                    rs.close();
                    pstmt.close();
                } catch (SQLException e) {
                    System.out.println("查询出错：" + e.getMessage());
                    System.out.println("是否重试？(1:是/0:否)");
                    if (in.nextInt() != 1) {
                        return;
                    }
                    in.nextLine();
                }
            }

            // 2.3 通过ID查询学生
            boolean studentFound = false;
            while (!studentFound) {
                try {
                    System.out.println("请输入一个0~99999的整数");
                    int num = in.nextInt();
                    if (num < 0 || num > 99999) {
                        System.out.println("输入的数字超出范围，请重试");
                        continue;
                    }

                    String sql2_3 = "SELECT * FROM student WHERE id = ?";
                    PreparedStatement pstmt2_3 = c.prepareStatement(sql2_3);
                    pstmt2_3.setInt(1, num);
                    ResultSet rs2_3 = pstmt2_3.executeQuery();

                    if (!rs2_3.isBeforeFirst()) {
                        System.out.println("未找到该学生，是否重试？(1:是/0:否)");
                        if (in.nextInt() != 1) {
                            return;
                        }
                        continue;
                    }

                    while (rs2_3.next()) {
                        studentFound = true;
                        String studentId2_3 = rs2_3.getString("ID");
                        String studentName2_3 = rs2_3.getString("name");
                        String studentDept2_3 = rs2_3.getString("dept_name");
                        int studentCred2_3 = rs2_3.getInt("tot_cred");
                        System.out.println("ID: " + studentId2_3 +
                                ", Name: " + studentName2_3 +
                                ", Department: " + studentDept2_3 +
                                ", Total Credits: " + studentCred2_3);
                    }

                    // 2.4 查询课程信息
                    if (studentFound) {
                        while (true) {
                            System.out.println("\n输入1查看该学生所修读的所有课程信息，输入0退出：");
                            int choice = in.nextInt();
                            if (choice == 0) {
                                return;
                            }
                            if (choice == 1) {
                                break;
                            }
                            System.out.println("输入无效，请重试");
                        }

                        String courseQuery =
                                "SELECT c.course_id, t.year, t.semester, c.title, c.dept_name, t.grade, c.credits " +
                                        "FROM takes t " +
                                        "JOIN course c ON t.course_id = c.course_id " +
                                        "WHERE t.ID = ? ";

                        PreparedStatement pstmtCourse = c.prepareStatement(courseQuery);
                        pstmtCourse.setInt(1, num);
                        ResultSet rsCourse = pstmtCourse.executeQuery();
                        Double totalGrade = 0.0;
                        int totalCredits = 0;
                        boolean hasEnrollments = false;

                        System.out.println("\n该学生的课程信息：\n");
                        while (rsCourse.next()) {
                            hasEnrollments = true;
                            String course_id2_4 = rsCourse.getString("course_id");
                            String year2_4 = rsCourse.getString("year");
                            String semester2_4 = rsCourse.getString("semester");
                            String title2_4 = rsCourse.getString("title");
                            String dept_name2_4 = rsCourse.getString("dept_name");
                            String grade2_4 = rsCourse.getString("grade");
                            int credits2_4 = rsCourse.getInt("credits");

                            System.out.println("课程ID: " + course_id2_4 +
                                    ", 上课年份: " + year2_4 +
                                    ", 上课学期: " + semester2_4 +
                                    ", 课程名称: " + title2_4 +
                                    ", 开课院系: " + dept_name2_4 +
                                    ", 成绩等级: " + grade2_4 +
                                    ", 课程学分数: " + credits2_4);

                            if (grade2_4 != null) {
                                String averageGradeQuery =
                                        "SELECT grade_point " +
                                                "FROM gpa " +
                                                "WHERE grade = ? ";
                                PreparedStatement pstmtGrade = c.prepareStatement(averageGradeQuery);
                                pstmtGrade.setString(1, grade2_4.trim().toUpperCase());
                                ResultSet rsGrade = pstmtGrade.executeQuery();
                                while (rsGrade.next()) {
                                    totalGrade += rsGrade.getDouble("grade_point") * credits2_4;
                                    totalCredits += credits2_4;
                                }
                                rsGrade.close();
                                pstmtGrade.close();
                            }
                        }

                        // 2.5 计算平均绩点
                        if (hasEnrollments && totalCredits > 0) {
                            while (true) {
                                System.out.println("\n输入1查看该学生所修读的所有课程的平均绩点,输入0退出：");
                                int choice1 = in.nextInt();
                                if (choice1 == 0) {
                                    return;
                                }
                                if (choice1 == 1) {
                                    Double averageGrade = totalGrade / totalCredits;
                                    //System.out.println("总绩点：" + totalGrade + ", 总学分：" + totalCredits);
                                    System.out.printf("该学生的平均绩点为%.2f%n", averageGrade);
                                    break;
                                }
                                System.out.println("输入无效，请重试");
                            }
                        } else {
                            System.out.println("该学生暂无有效的课程成绩记录");
                        }

                        rsCourse.close();
                        pstmtCourse.close();
                    }
                    rs2_3.close();
                    pstmt2_3.close();
                } catch (SQLException e) {
                    System.out.println("查询出错：" + e.getMessage());
                    System.out.println("是否重试？(1:是/0:否)");
                    if (in.nextInt() != 1) {
                        return;
                    }
                }
            }
        } catch (Exception e) {
            System.out.println("程序出错：" + e.getMessage());
        } finally {
            try {
                if (stmt != null) stmt.close();
                if (c != null) c.close();
                if (in != null) in.close();
            } catch (SQLException e) {
                System.out.println("关闭资源时出错：" + e.getMessage());
            }
        }
    }
}