package contest;

public class Tile {
    private char character;
    private int x_col;
    private int y_row;

    public Tile(char character, int x_col, int y_row) {
        this.character = character;
        this.x_col = x_col;
        this.y_row = y_row;
    }

    public char getCharacter() {
        return character;
    }

    public void setCharacter(char character) {
        this.character = character;
    }

    public int getX_col() {
        return x_col;
    }

    public void setX_col(int x_col) {
        this.x_col = x_col;
    }

    public int getY_row() {
        return y_row;
    }

    public void setY_row(int y_row) {
        this.y_row = y_row;
    }

    @Override
    public String toString() {
        return character + "(" + x_col + "," + y_row + ")";
    }
}
