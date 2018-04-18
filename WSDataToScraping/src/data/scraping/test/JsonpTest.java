package data.scraping.test;


import java.io.IOException;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

public class JsonpTest {

	public static void main(String[] args) throws IOException {
		Document document = Jsoup.connect("https://ws-tcg.com/cardlist/search").get();
		System.out.println(document.html());
		// 20180417end
		//TODO get ws card list
		//TODO get card list insert to ws_db
		//TODO know about jsoup library method
	}
}
