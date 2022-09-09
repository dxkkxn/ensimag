public class TestRational {
    public static void main(String[] args) {
        //Rational r = null;
        Rational r = new Rational();
        //System.out.println("rational r = " + r.num + "/" + r.denom);
        System.out.println("rational r = " +  r); 
        r.setNum(3);
        r.setDenom(2);
        //System.out.println("rational r = " + r.num + "/" + r.denom);
        System.out.println("rational r = " + r);
        r.setDenom(0);
    }
}
