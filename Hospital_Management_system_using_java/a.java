import java.util.*;
class a
{
	public static void main(String args[])
	{
		Scanner sc=new Scanner(System.in);
		System.out.print("enter string");
		String s=sc.nextLine();
		String rev="";
		for(int i=s.length()-1;i>=0;i--)
		{
			rev=rev+s.charAt();
		}
		
	}
}