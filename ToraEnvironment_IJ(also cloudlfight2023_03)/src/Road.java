public class Road {
    private int cityA, cityB;
    private int distance;

    public Road(int cityA, int cityB, int distance) throws InvalidInputDataException{
        if(cityA >= 0 && cityA <= 1000) {
            this.cityA = cityA;
        } else throw new InvalidInputDataException("Invalid road description");

        if(cityB >= 0 && cityB <= 1000) {
            this.cityB = cityB;
        } else throw new InvalidInputDataException("Invalid road description");

        if(distance >= 1 && distance <= 1000) {
            this.distance = distance;
        } else throw new InvalidInputDataException("Invalid distance value");
    }

    public int getCityA() {
        return cityA;
    }

    public void setCityA(int cityA) throws InvalidInputDataException {
        if(cityA >= 0 && cityA <= 1000) {
            this.cityA = cityA;
        } else throw new InvalidInputDataException("Invalid road description");
    }

    public int getCityB() {
        return cityB;
    }

    public void setCityB(int cityB) throws InvalidInputDataException {
        if(cityB >= 0 && cityB <= 1000) {
            this.cityB = cityB;
        } else throw new InvalidInputDataException("Invalid road description");
    }

    public int getDistance() {
        return distance;
    }

    public void setDistance(int distance) throws InvalidInputDataException{
        if(distance >= 1 && distance <= 1000) {
            this.distance = distance;
        } else throw new InvalidInputDataException("Invalid distance value");
    }
}
