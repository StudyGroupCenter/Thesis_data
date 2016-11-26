package demo;

import java.io.*;

public class ProcessingFile{

	public static void main(String[] args) throws Exception{
		// TODO Auto-generated method stub
		File f3 = new File("why.txt");
		int len = 0;
//		OutputStream out = new FileOutputStream(f3, true);
//		String info="hello";
//		byte[] bytes=info.getBytes();
//		out.write(bytes);
//		out.close();
		
//		InputStream In = null;
//		In = new FileInputStream(f3);
//		byte[] b=new byte[1024];
//		len=In.read(b);
//		In.close();
//		System.out.println(new String(b, 0, len));
		
		
//		Writer write = new FileWriter(f3, true);
//		String info = "hello, i am sb";
//		write.write(info);
//		write.close();
		BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(f3)));
		String my=br.readLine();
		br.close();
		System.out.println(my);
	}
}
