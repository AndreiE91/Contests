import java.util.ArrayList;
import java.util.TreeMap;

public class Scenario {
    private int nCities, mRoads, initialGoldAmount;
    private ArrayList<Road> roads;
    private TreeMap<Integer,Integer> sellPrices;
    private int priceBuyProductInCity0;

    public Scenario(int nCities, int mRoads, int initialGoldAmount, int priceBuyProductInCity0) throws InvalidInputDataException {
        if(nCities >= 0 && nCities <= 1000) {
            this.nCities = nCities;
        } else throw new InvalidInputDataException("Invalid number of cities");

        if(mRoads >= 0 && mRoads <= 2000) {
            this.mRoads = mRoads;
        } else throw new InvalidInputDataException("Invalid number of roads");

        if(initialGoldAmount >= 0 && initialGoldAmount <= 1000) {
            this.initialGoldAmount = initialGoldAmount;
        } else throw new InvalidInputDataException("Invalid initialGoldAmount value");

        if(priceBuyProductInCity0 >= 13 && priceBuyProductInCity0 <= 10000) {
            this.priceBuyProductInCity0 = priceBuyProductInCity0;
        } else throw new InvalidInputDataException("Invalid value for buy price");

        this.roads = new ArrayList<Road>();
        this.sellPrices = new TreeMap<Integer,Integer>();
    }

    public Scenario(int nCities, int mRoads, int initialGoldAmount) throws InvalidInputDataException {
        if(nCities >= 0 && nCities <= 1000) {
            this.nCities = nCities;
        } else throw new InvalidInputDataException("Invalid number of cities");

        if(mRoads >= 0 && mRoads <= 2000) {
            this.mRoads = mRoads;
        } else throw new InvalidInputDataException("Invalid number of roads");

        if(initialGoldAmount >= 0 && initialGoldAmount <= 1000) {
            this.initialGoldAmount = initialGoldAmount;
        } else throw new InvalidInputDataException("Invalid initialGoldAmount value");

        this.roads = new ArrayList<Road>();
        this.sellPrices = new TreeMap<Integer,Integer>();
    }

    public int getnCities() {
        return nCities;
    }

    public void setnCities(int nCities) throws InvalidInputDataException {
        if(nCities >= 0 && nCities <= 1000) {
            this.nCities = nCities;
        } else throw new InvalidInputDataException("Invalid number of cities");
    }

    public int getmRoads() {
        return mRoads;
    }

    public void setmRoads(int mRoads) throws InvalidInputDataException {
        if(mRoads >= 0 && mRoads <= 2000) {
            this.mRoads = mRoads;
        } else throw new InvalidInputDataException("Invalid number of roads");
    }

    public int getInitialGoldAmount() {
        return initialGoldAmount;
    }

    public void setInitialGoldAmount(int initialGoldAmount) throws InvalidInputDataException {
        if(initialGoldAmount >= 0 && initialGoldAmount <= 1000) {
            this.initialGoldAmount = initialGoldAmount;
        } else throw new InvalidInputDataException("Invalid initialGoldAmount value");
    }

    public int getPriceBuyProductInCity0() {
        return priceBuyProductInCity0;
    }

    public void setPriceBuyProductInCity0(int priceBuyProductInCity0) throws InvalidInputDataException {
        if(priceBuyProductInCity0 >= 13 && priceBuyProductInCity0 <= 10000) {
            this.priceBuyProductInCity0 = priceBuyProductInCity0;
        } else throw new InvalidInputDataException("Invalid value for buy price");
    }

    public ArrayList<Road> getRoads() {
        return roads;
    }

    public void setRoads(ArrayList<Road> roads) {
        this.roads = roads;
    }

    public TreeMap<Integer, Integer> getSellPrices() {
        return sellPrices;
    }

    public void setSellPrices(TreeMap<Integer, Integer> sellPrices) {
        this.sellPrices = sellPrices;
    }
}
