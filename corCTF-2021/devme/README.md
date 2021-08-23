![image](https://user-images.githubusercontent.com/44206101/130443090-2cbfaadb-3a4f-4236-b0ac-77879c50fd5a.png)
# First look
After accessing this url `https://devme.be.ax`, take seconds to see that there a email input at the bottom of the website.
![image](https://user-images.githubusercontent.com/44206101/130443620-4931dbf4-d1f3-48c0-b6ca-0b889fe14712.png)
So i decided to use Burp Suite to understand how it works.
# Burp Suite
After fill the email, i received this message:
![image](https://user-images.githubusercontent.com/44206101/130444250-39592964-6b92-4a38-a90b-a789f672971f.png)
Now, let's check HTTP history in Burp Suite.
![image](https://user-images.githubusercontent.com/44206101/130444518-95887fb1-07ce-448a-ac8b-e1f82981840d.png)
It's obvious that there something suspicious in `https://devme.be.ax/graphql`, maybe it's a graphql injection.
![image](https://user-images.githubusercontent.com/44206101/130445241-e6539b44-b1e5-4e73-8457-98d187bf4447.png)
I used InQL Scanner, an extention in Burp Suite and it gave me usable queries, fields.
![image](https://user-images.githubusercontent.com/44206101/130445793-59af1650-c706-4770-8c82-7ba19992f0d4.png)
