public class TestVector{
    public static void main(String[] args) {
        //Rational r = new Rational(10, 20);
        //Rational r2 = new Rational(30, 20);
        //Vector v = new Vector(2);
        //v.set(0, r); v.set(1, r2);
        //System.out.println("vector v = " + v);
        ////r.mult(r1);
        //r.sum(r1);
        //System.out.println("rational r = " + r);
        //System.out.println("rational r = " + r.num + "/" + r.denom);
        // System.out.println("rational r = " +  r); 
        //System.out.println("rational r = " + r.num + "/" + r.denom);
        // r.setDenom(0);
        Rational r = new Rational(0, 1);
        Rational r2 = new Rational(0, 1);
        Vector v = new Vector(2);
        v.set(0, r); v.set(1, r2);
        System.out.println("v = " + v);
        Rational a = new Rational(2, 3);
        v.set(0, a);
        System.out.println("v = " + v);
        Rational b = new Rational(3, 2);
        a.mult(b);
        System.out.println("v = " + v);


    }
}
