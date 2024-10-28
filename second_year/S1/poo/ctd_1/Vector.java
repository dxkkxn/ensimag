class Vector{
    private Rational[] arr;
    public Vector(int size) {
        this.arr = new Rational[size];
    }
    @Override
    public String toString() {
        String res = "[";
        for (int i = 0; i < this.arr.length- 1; i++) {
            res += (this.arr[i] + ", ");
        }
        res += (this.arr[this.arr.length - 1]+"]");
        return res;
    }
    void set(int i, Rational r) {
        System.out.println(i + " " + this.arr.length);
        Rational r_copy = new Rational(r.getNum(), r.getDenom());
        if (i >= this.arr.length) {
            throw new IllegalArgumentException("Index out of range");
        }
        this.arr[i] = r;
    }
}
