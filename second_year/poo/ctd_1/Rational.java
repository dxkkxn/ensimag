class Rational {
    private int num;
    private int denom;

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
}
