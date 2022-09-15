class Rational {
    private int num;
    private int denom;

    private int pgcd(int a, int b) {
        if (b == 0) {
            return a;
        } else {
            return pgcd(b, a%b);
        }
    }
    private void reduce() {
        int pgcd_ ;
        if ((pgcd_ = pgcd(this.num, this.denom)) != 1) {
            this.num /= pgcd_;
            this.denom /= pgcd_;
        }
    }

    public Rational(int num, int denom) {
        this.num = num;
        this.denom = denom;
        reduce();
    }

    @Override
    public String toString() {
        return this.num + " / " + this.denom;
    }

    public void setNum(int num) {
        this.num = num;
        this.denom = denom;
    }

    public void setDenom(int denom) {
        if (denom == 0) {
            throw new IllegalArgumentException("Denom can't be zero");
        }
        this.denom = denom;
    }
    public void mult(Rational r) {
        this.num *= r.num;
        this.denom *= r.denom;
        reduce();
    }
    public void sum(Rational r) {
        this.num += r.num;
        this.denom += r.denom;
        reduce();
    }
    public int getNum() {
        return this.num;
    }
    public int getDenom() {
        return this.denom;
    }
}
