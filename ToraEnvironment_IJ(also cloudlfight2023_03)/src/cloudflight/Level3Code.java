package cloudflight;

import org.jgrapht.Graph;
import org.jgrapht.GraphPath;
import org.jgrapht.Graphs;
import org.jgrapht.alg.interfaces.ShortestPathAlgorithm;
import org.jgrapht.alg.shortestpath.BFSShortestPath;
import org.jgrapht.alg.shortestpath.DijkstraShortestPath;
import org.jgrapht.generate.GridGraphGenerator;
import org.jgrapht.graph.DefaultEdge;
import org.jgrapht.graph.DefaultWeightedEdge;
import org.jgrapht.graph.SimpleGraph;
import org.jgrapht.graph.SimpleWeightedGraph;

import java.io.*;
import java.util.*;

public class Level3Code {
    public static void main(String[] args) {

        //Step 1: Fetch data from file
        String inputFilePath = "level4_1.in"; // set the name of the input file
        String outputFilePath = "level4_1_out.out"; // set the name of the output file

        int nFights = 0;
        int mFightersTournament = 0;

        try (BufferedReader reader = new BufferedReader(new FileReader(inputFilePath))) {
            PrintWriter writer = new PrintWriter(new FileWriter(outputFilePath));

            String line;

            //Read number of scenarios
            if((line = reader.readLine()) != null) {
                String splits[] = line.split(" ");
                nFights = Integer.parseInt(splits[0]);
                mFightersTournament = Integer.parseInt(splits[1]);
            }

            ArrayList<RockPaperScissorsPair> tournamentSetups = new ArrayList<>();
            //Read line by line each tournament
            for(int i = 0; i < nFights; ++i) {
                if ((line = reader.readLine()) != null) {
                    String[] substrings = line.split(" ");
                    //Remove letters for parsing purposes
                    for(int j = 0; j < substrings.length; ++j) {
                        substrings[j] = substrings[j].substring(0, substrings[j].length() - 1);
                    }
                    tournamentSetups.add(new RockPaperScissorsPair(Integer.parseInt(substrings[0]), Integer.parseInt(substrings[1]), Integer.parseInt(substrings[2])));
                }
            }
            int index = 0;
            for(RockPaperScissorsPair tournamentSetup : tournamentSetups) {
                String tempLine = new String();
                int currNumberRock = tournamentSetup.getNumberRock();
                int currNumberPaper = tournamentSetup.getNumberPaper();
                int currNumberScissors = tournamentSetup.getNumberScissors();
                System.out.println(index + ": " + "R:" + currNumberRock + " P:" + currNumberPaper + " S:" + currNumberScissors);
                ++index;
                while(currNumberRock > 1) {
                    if(currNumberRock == 2) {
                        if(currNumberScissors > 1) {
                            tempLine += "RS";
                            --currNumberRock;
                            --currNumberScissors;
                            if(currNumberPaper > 0) {
                                tempLine += "RP";
                                --currNumberPaper;
                                --currNumberRock;
                            }
                        } else {
                            tempLine += "RR";
                            currNumberRock -= 2;
                            if (currNumberPaper > 0) {
                                if (currNumberRock > 0) {
                                    tempLine += "RP";
                                    --currNumberRock;
                                    --currNumberPaper;
                                }
                            }
                        }
                    } else {
                        tempLine += "RR";
                        currNumberRock -= 2;
                        if (currNumberPaper > 0) {
                            if (currNumberRock > 0) {
                                tempLine += "RP";
                                --currNumberRock;
                                --currNumberPaper;
                            }
                        }
                    }
                }
                if(currNumberRock >= 1) {
                    if(currNumberPaper > 0) {
                        tempLine += "RP";
                        --currNumberRock;
                        --currNumberPaper;
                    }
                }
                //Aici rock e 0 garantat
                while(currNumberPaper > 1) {
                    tempLine += "PP";
                    currNumberPaper -= 2;
                }
                if(currNumberPaper == 1) {
                    tempLine += "PS";
                    --currNumberPaper;
                    --currNumberScissors;
                }
                while(currNumberScissors > 1) {
                    tempLine += "SS";
                    currNumberScissors -= 2;
                }
                if(currNumberScissors > 0) {
                    tempLine += "SS";
                    --currNumberScissors;
                }
                if(currNumberRock != 0 || currNumberPaper != 0 || currNumberScissors != 0) {
                    System.out.println("Bad");
                }
                writer.println(tempLine);
            }

            reader.close(); // close the Reader object to flush the buffer and release the resources
            writer.close(); // close the PrintWriter object to flush the buffer and release the resources
        } catch (IOException e) {
            System.err.println("Error reading file: " + e.getMessage());
        }
    }

    static char getWinner(char fighter1, char fighter2) {
        if(fighter1 == fighter2) {
            return fighter1;
        } else if(fighter1 == 'R' && fighter2 == 'P') {
            return fighter2;
        } else if(fighter1 == 'R' && fighter2 == 'S') {
            return fighter1;
        } else if(fighter1 == 'S' && fighter2 == 'P') {
            return fighter1;
        } else if(fighter1 == 'S' && fighter2 == 'R') {
            return fighter2;
        } else if(fighter1 == 'P' && fighter2 == 'R') {
            return fighter1;
        } else if(fighter1 == 'P' && fighter2 == 'S') {
            return fighter2;
        } else {
            System.out.println("ERROR IN GETTING WINNER!");
            return 'E';
        }
    }
}
