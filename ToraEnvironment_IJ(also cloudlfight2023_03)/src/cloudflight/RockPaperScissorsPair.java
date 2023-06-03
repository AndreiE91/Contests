package cloudflight;

public class RockPaperScissorsPair {
    private int numberRock, numberPaper, numberScissors;

    public RockPaperScissorsPair(int numberRock, int numberPaper, int numberScissors) {
        this.numberRock = numberRock;
        this.numberPaper = numberPaper;
        this.numberScissors = numberScissors;
    }

    public int getNumberRock() {
        return numberRock;
    }

    public void setNumberRock(int numberRock) {
        this.numberRock = numberRock;
    }

    public int getNumberPaper() {
        return numberPaper;
    }

    public void setNumberPaper(int numberPaper) {
        this.numberPaper = numberPaper;
    }

    public int getNumberScissors() {
        return numberScissors;
    }

    public void setNumberScissors(int numberScissors) {
        this.numberScissors = numberScissors;
    }
}
