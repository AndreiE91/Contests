public class City {
    private int id;
    private int sellPrice;

    private double profitPerUnitOfTime;

    public City(int id, int sellPrice) {
        this.id = id;
        this.sellPrice = sellPrice;
    }

    public double getProfitPerUnitOfTime() {
        return profitPerUnitOfTime;
    }

    public void setProfitPerUnitOfTime(double profitPerUnitOfTime) {
        this.profitPerUnitOfTime = profitPerUnitOfTime;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getSellPrice() {
        return sellPrice;
    }

    public void setSellPrice(int sellPrice) {
        this.sellPrice = sellPrice;
    }
}
