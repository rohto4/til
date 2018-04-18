package data.scraping.test;


import java.io.IOException;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class JsonpTest {

	public static void main(String[] args) throws IOException {

		String url = "https://ws-tcg.com/cardlist/search";
		try {
			Document doc = Jsoup.connect(url).get();


			// unitクラスを取得
			Elements unitClass = doc.select("tr");
			int i = 0;
			for (Element element : unitClass) {
				i++;
				System.out.println(i + "----------");
				System.out.println(element.outerHtml());
			}
		} catch (IOException e) {
			e.printStackTrace();
		}

		//TODO get ws card list
		//TODO get card list insert to ws_db
		//TODO know about jsoup library method
	}



}

