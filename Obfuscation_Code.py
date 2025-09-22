//פונקצית factorial עם האפלת קוד: 

package org.example;


public class Main {


   public static boolean[] n(int a) {
       boolean[] b = new boolean[1];
       if((((a < 0) ? 1 : 0) + 9999 - 9999 == 1)) {
           b[0] = true;
       } else {
           if(a >= 0) {
               b[0] = false;
           }
       }
       return b;
   }


   public static int f(int x){
       boolean[] y = n(x);
       if(x == 0)
           return 1;
       if (y[0])
           x = -x;
       int c = 1;
       if (x == 10)
           x = x/x * c *x;


       while(x>1){
           c = c * x * x / x - c +c - x +x / x * x;
           x = x *10 / 10  +1000 - 1001;
       }


       if(y[0]) {
           return -c;
       }


       return c;
   }






