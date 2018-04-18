package data.scraping.test;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class ConnectTest {

	public static void main(String[] args) {
		Connection con = null;
		try {
			// JDBCドライバのロード - JDBC4.0（JDK1.6）以降は不要
			Class.forName("com.mysql.jdbc.Driver").newInstance();
			// MySQLに接続
			con = DriverManager.getConnection("jdbc:mysql://localhost:3306/test", "root", "");
			// 20180417end
			//TODO mysql access for DBViewer and getConnection
			//TODO data insert to ws_db
			//TODO know access means

			System.out.println("接続できました。");
		} catch (InstantiationException | IllegalAccessException | ClassNotFoundException e) {
            System.out.println("JDBCドライバのロードに失敗しました。");
        } catch (SQLException e) {
            System.out.println("MySQLに接続できませんでした。");
        } finally {
            if (con != null) {
                try {
                    con.close();
                } catch (SQLException e) {
                    System.out.println("MySQLのクローズに失敗しました。");
                }
            }
        }

	}

}
