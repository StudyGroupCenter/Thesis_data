package demo;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.nio.file.Paths;
import java.util.Date;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.cjk.*;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.FSDirectory;

public class SearchTest {

	public static void main(String[] args) throws Exception {
	    String index = "";
	    String queryPath = "";
	    String outPath = "";
	    for(int i=0;i<args.length;i++) {
	        if ("-index".equals(args[i])) {
	          index = args[i+1];
	          i++;
	        } else if ("-query".equals(args[i])) {
	          queryPath = args[i+1];
	          i++;
	        } else if ("-out".equals(args[i])) {
	          outPath = args[i+1];
	          i++;
	        }
	    }
	    String field = "html";
	    //String queries = null;
	    int repeat = 1;
	    //boolean raw = false;
	    int count=0;
	    
	    String queryString = null;
	    //int hitsPerPage = 10;
	    
	    IndexReader reader = DirectoryReader.open(FSDirectory.open(Paths.get(index)));
	    IndexSearcher searcher = new IndexSearcher(reader);
	    Analyzer analyzer = new CJKAnalyzer();

	    BufferedReader in = null;
	    BufferedWriter out =null;
	    String actualQuery;
	    
	    in = new BufferedReader(new InputStreamReader(new FileInputStream(queryPath)));
	    out = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(outPath, true)));
	    
	    
	    QueryParser parser = new QueryParser(field, analyzer);
	    while (true) {
	      count++;
	      String line = in.readLine();
	      if (line == null || line.length() == -1) {
	        break;
	      }
	      line = line.trim();
	      if (line.length() == 0) {
	        break;
	      }
	      String myQuery = line.split(" ")[1];
	      if(myQuery.length()>48)
	    	  actualQuery=myQuery.substring(0, 48).replace('_',' ');
	      else actualQuery=myQuery.replace('_', ' ');
	      Query query;
	      try{
	      query = parser.parse(actualQuery);
	      }catch(Exception e)
	      {
	    	  continue;
	      }
	      
	      //System.out.println("Searching for: " + query.toString(field));     
	      if (repeat > 0) {                           // repeat & time as benchmark
	        Date start = new Date();
	        for (int i = 0; i < repeat; i++) {
	          searcher.search(query, null, 30);
	        }
	        Date end = new Date();
	        //System.out.println("Time: "+(end.getTime()-start.getTime())+"ms");
	        out.write(line+" "+(end.getTime()-start.getTime())+"\n");
	      }
	      if(count%1000==0)
	      {
	    	  count=0;
	    	  out.flush();
	      }
	      //doPagingSearch(in, searcher, myQuery, hitsPerPage, raw, false);
	      if (queryString != null) {
	        break;
	      }
	    }
	    in.close();
	    reader.close();
	    out.close();
	  }

	  /**
	   * This demonstrates a typical paging search scenario, where the search engine presents 
	   * pages of size n to the user. The user can then go to the next page if interested in
	   * the next hits.
	   * 
	   * When the query is executed for the first time, then only enough results are collected
	   * to fill 5 result pages. If the user wants to page beyond this limit, then the query
	   * is executed another time and all hits are collected.
	   * 
	   */
	  public static void doPagingSearch(BufferedReader in, IndexSearcher searcher, Query query, 
	                                     int hitsPerPage, boolean raw, boolean interactive) throws IOException {
	 
	    // Collect enough docs to show 3 pages
	    TopDocs results = searcher.search(query, 3 * hitsPerPage);
	    ScoreDoc[] hits = results.scoreDocs;
	    
	    int numTotalHits = results.totalHits;
	    System.out.println(numTotalHits + " total matching documents");

	    int start = 0;
	    int end = Math.min(numTotalHits, hitsPerPage);
	        
	    while (true) {
	      if (end > hits.length) {
	        System.out.println("Only results 1 - " + hits.length +" of " + numTotalHits + " total matching documents collected.");
	        System.out.println("Collect more (y/n) ?");
	        String line = in.readLine();
	        if (line.length() == 0 || line.charAt(0) == 'n') {
	          break;
	        }

	        hits = searcher.search(query, numTotalHits).scoreDocs;
	      }
	      
	      end = Math.min(hits.length, start + hitsPerPage);
	      
	      for (int i = start; i < end; i++) {
	        if (raw) {                              // output raw format
	          System.out.println("doc="+hits[i].doc+" score="+hits[i].score);
	          continue;
	        }

	        Document doc = searcher.doc(hits[i].doc);
	        String path = doc.get("url");
	        if (path != null) {
	          System.out.println((i+1) + ". " + path + ",score:" + hits[i].score);
	        } else {
	          System.out.println((i+1) + ". " + "No path for this document");
	        }
	                  
	      }

	      if (!interactive || end == 0) {
	        break;
	      }

	      if (numTotalHits >= end) {
	        boolean quit = false;
	        while (true) {
	          System.out.print("Press ");
	          if (start - hitsPerPage >= 0) {
	            System.out.print("(p)revious page, ");  
	          }
	          if (start + hitsPerPage < numTotalHits) {
	            System.out.print("(n)ext page, ");
	          }
	          System.out.println("(q)uit or enter number to jump to a page.");
	          
	          String line = in.readLine();
	          if (line.length() == 0 || line.charAt(0)=='q') {
	            quit = true;
	            break;
	          }
	          if (line.charAt(0) == 'p') {
	            start = Math.max(0, start - hitsPerPage);
	            break;
	          } else if (line.charAt(0) == 'n') {
	            if (start + hitsPerPage < numTotalHits) {
	              start+=hitsPerPage;
	            }
	            break;
	          } else {
	            int page = Integer.parseInt(line);
	            if ((page - 1) * hitsPerPage < numTotalHits) {
	              start = (page - 1) * hitsPerPage;
	              break;
	            } else {
	              System.out.println("No such page");
	            }
	          }
	        }
	        if (quit) break;
	        end = Math.min(numTotalHits, start + hitsPerPage);
	      }
	    }
	  }
}
